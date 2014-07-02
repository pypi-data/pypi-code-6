""" goulash.tests.test_metaclasses
"""
import unittest
from inspect import isclass
from goulash.metaclasses import ClassAlgebra


class TestClass(object):
    __metaclass__ = ClassAlgebra
    def test_method(self):
        return 'base-method'

class Mixin(object):
    def mixin_method(self):
        return 'unique-mixin-method'
    def test_method(self):
        return 'mixin-override'

class TestClassAlgebra(unittest.TestCase):
    def setUp(self):
        self.kls = TestClass
        self.mixin = Mixin

    def assertIsClass(self, other, err=None):
        err = err or 'expected {0} would be a class object'.format(other)
        return self.assertTrue(isclass(other), err)
    assertClass = assertIsClass

    def test_subclass(self):
        new_method = lambda himself: 42
        new_kls = self.kls.subclass('MySubclass',new_method=new_method)
        err = 'expected .subclass() would result in a new class'
        self.assertClass(new_kls, err)
        err = 'expected result of .subclass() would support class-algebra'
        self.assertEqual(type(new_kls), ClassAlgebra, err)
        err = 'expected new_method() would work as passed!'
        self.assertEqual(new_kls().new_method(), 42)

    def test_right_mix(self):
        tmp = TestClass >> Mixin
        self.assertClass(tmp)
        expected = (TestClass, Mixin)
        actual = tmp.__bases__
        err = 'expected right-mix would result in bases: ' + str(expected)
        self.assertEqual(expected, actual, err)
        err = 'MRO is broken with right-mix operation'
        self.assertEqual(tmp().test_method(), 'base-method', err)
        self.assertEqual(tmp().mixin_method(), 'unique-mixin-method')

    def test_left_mix(self):
        tmp = TestClass << Mixin
        expected = (Mixin, TestClass)
        actual = tmp.__bases__
        err = 'expected left-mix would result in bases: ' + str(expected)
        self.assertEqual(expected, actual, err)
        err = 'MRO is broken with lefte-mix operation'
        self.assertEqual(tmp().test_method(), 'mixin-override', err)
        self.assertEqual(tmp().mixin_method(), 'unique-mixin-method')


if __name__=='__main__':
    unittest.main()
