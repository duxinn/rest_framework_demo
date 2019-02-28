from django.test import TestCase


class Foo(object):
    def __init__(self, a1):
        self.a1 = a1

    def __new__(cls, *args, **kwargs):
        """
        1.根据类创建对象
        2.执行返回值__init__
        :param args:
        :param kwargs:
        :return:
        """
        print(cls)
        return object.__init__(cls)

