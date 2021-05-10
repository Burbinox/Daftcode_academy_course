import unittest


def add_class_method(cls):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, staticmethod(wrapper))
        return func
    return decorator


def add_instance_method(cls):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator


class ExampleClass:
    pass


@add_class_method(ExampleClass)
def cls_method():
    return "Hello!"


@add_instance_method(ExampleClass)
def inst_method():
    return "Hello!"


class ExampleTest(unittest.TestCase):
    def test_result(self):
        self.assertEqual(ExampleClass.cls_method(), cls_method())
        self.assertEqual(ExampleClass().inst_method(), inst_method())


if __name__ == "__main__":
    unittest.main()