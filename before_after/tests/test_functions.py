test_list = []

def reset_test_list():
    del test_list[:]

def sample_fn(arg):
    print('sample', arg)
    test_list.append(arg)


class Sample(object):
    CLASS_LIST = []

    def __init__(self):
        self.instance_list = []

    def method(self, arg):
        print('Sample.method', arg)
        self.instance_list.append(arg)

    def method_with_exception(self, arg):
        self.method(arg)
        raise Exception

    @classmethod
    def class_method(cls, arg):
        print('Sample.class_method', arg)
        cls.CLASS_LIST.append(arg)
