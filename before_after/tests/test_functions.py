test_list = []

def reset_test_list():
    del test_list[:]

def sample_fn(arg):
    print 'sample', arg
    test_list.append(arg)


class Sample(object):
    def method(self, arg):
        print 'Sample.method'
        test_list.append(arg)
