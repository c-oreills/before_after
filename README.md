# before_after
before_after provides utilities to help test race conditions.

When testing Python programs that run in multiple threads or processes it's useful to simulate race conditions to ensure you handle them properly. before_after provides two functions, `before` and `after`, that allow you to insert pre or post functions to be called before/after a function you want to test.

See this [blog post](http://www.oreills.co.uk/2015/03/01/testing-race-conditions-in-python.html) for a practical example of using before_after in tests.

## Patching

before_after is sugar over the [Mock library](http://www.voidspace.org.uk/python/mock/). It's recommended that you read the docs before using before_after, especially [Where to patch](http://www.voidspace.org.uk/python/mock/patch.html#where-to-patch).

## Example usage
[Practical example of testing race conditions](http://www.oreills.co.uk/2015/03/01/testing-race-conditions-in-python.html)

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

## Use with methods

Since v1.0.0 before_after can be used on function methods. Make sure your before_fn/after_fn accepts a `self` argument.

    class Greeter(object):
        def __init__(self):
            self.greeted = []

        def greet(self, name):
            print 'Hi there', name
            self.greeted.append(name)
            print 'This is now a party of', len(self.greeted)

    def after_fn(self, name):
        self.greet("{name}'s guest".format(name=name))

    greeter = Greeter()

    with before_after.after('__main__.Greeter.greet', after_fn):
        greeter.greet('Alice')

    # Hi there Alice
    # This is now a party of 1
    # Hi there Alice's guest
    # This is now a party of 2
