# before_after
before_after provides utilities to help test race conditions.

When testing Python programs that run in multiple threads or multiple processes it can be useful to simulate race conditions in tests, to ensure you handle them properly. before_after provides two functions, `before` and `after`, that allow you to insert pre or post functions that will be called before/after a function in your code.

See this [blog post](http://www.oreills.co.uk/2015/03/01/testing-race-conditions-in-python.html) for a practical example of using before_after in tests.

## Patching

before_after is sugar over the [Mock library](http://www.voidspace.org.uk/python/mock/). It's recommended that you read the docs before using before_after, especially [Where to patch](http://www.voidspace.org.uk/python/mock/patch.html#where-to-patch).

## Example usage

    def before_fn(*a, **k):
        print 'before_fn called with', a, k

    def after_fn(*a, **k):
        print 'after_fn called with', a, k

    def hello(name, greeting='Hello'):
        print '{greeting} {name}!'.format(
            greeting=greeting, name=name)

    with before_after.before('__main__.hello', before_fn):
        hello('World')

    # before_fn called with ('World',) {}
    # Hello World!

    with before_after.after('__main__.hello', after_fn):
        hello('everybody', greeting='Hi there')

    # Hi there everybody!
    # after_fn called with ('everybody',) {'greeting': 'Hi there'}

## Use with recursive functions

By default, before_after only calls the before_fn/after_fn function once. This is useful if you're calling the original function within the before_fn/after_fn, since otherwise you'll blow the stack. This behaviour can be disabled by passing `once=False`.

    my_list = []

    def before_fn(*a, **k):
        print 'calling my_append in before_fn'
        my_append(1)

    def my_append(item):
        print 'appending', item, 'to my_list'
        my_list.append(item)
        print 'my_list is now', my_list

    with before_after.before('__main__.my_append', before_fn):
        my_append(2)

    # calling my_append in before_fn
    # appending 1 to my_list
    # my_list is now [1]
    # appending 2 to my_list
    # my_list is now [1, 2]

    with before_after.before('__main__.my_append', before_fn, once=False):
        my_append(2)

    # calling my_append in before_fn
    # calling my_append in before_fn
    # calling my_append in before_fn
    # ...
    # RuntimeError: maximum recursion depth exceeded while calling a Python object

It's recommended that if you're passing `once=False` that you make sure your program will exit cleanly!
