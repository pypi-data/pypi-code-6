""" goulash.tests.test_decorators
"""

from unittest import TestCase
from goulash.decorators import arg_types, memoized_property

class TestArgTypesDecorator(TestCase):
    def setUp(self):
        self.fxn = lambda x: x

    def test_ignores_kargs(self):
        @arg_types(int)
        def fxn(*args, **kargs):
            return kargs
        fxn(1, 2, 3, foo='bar')

    def test_one_type_bad(self):
        tmp = arg_types(int)(self.fxn)
        self.assertRaises(
            arg_types.ArgTypeError,
            lambda: tmp('3'))

    def test_two_types_bad(self):
        tmp = arg_types(int,list)(self.fxn)
        self.assertRaises(
            arg_types.ArgTypeError,
            lambda: tmp('3'))

    def test_good_two_types(self):
        tmp = arg_types(int, list)(self.fxn)
        tmp(42)

    def test_good_one_type(self):
        tmp = arg_types(list)(self.fxn)
        tmp([])

class TestMemoizedProperty(TestCase):
    def setUp(self):
        self.call_count = 0
        class ExampleClass(object):
            @memoized_property
            def example(himself):
                self.call_count += 1
                return 3
        self.kls = ExampleClass

    def test_memoized_property(self):
        tmp1 = self.kls()
        tmp2 = self.kls()
        self.assertEqual(tmp1.example, 3)
        self.assertEqual(self.call_count, 1)
        self.assertEqual(tmp1.example, 3)
        self.assertEqual(self.call_count, 1)
        #note: different instances *should* get fresh calls
        self.assertEqual(tmp2.example, 3)
        self.assertEqual(self.call_count, 2)
        self.assertEqual(tmp1.example, 3)
        self.assertEqual(tmp2.example, 3)
        self.assertEqual(self.call_count, 2)
