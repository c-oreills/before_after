test_list = []

def reset_test_list():
    del test_list[:]

def sample_fn(arg):
    print 'sample', arg
    test_list.append(arg)


class Sample(object):
    def __init__(self):
        self.instance_list = []

    def method(self, arg):
        print 'Sample.method', arg
        self.instance_list.append(arg)
