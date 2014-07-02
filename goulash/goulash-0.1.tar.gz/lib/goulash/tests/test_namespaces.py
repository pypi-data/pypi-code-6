""" goulash.tests.test_namespaces
"""

from unittest import TestCase, main

from goulash import Namespace
from goulash.tests.data import TestObject, ComplexTestObject

class TestRecursive(TestCase):
    def setUp(self):
        self.obj = TestObject()
        self.ns = Namespace(self. obj, dictionaries=False)

    def test_original(self):
        self.assertEqual(self.obj, self.ns.obj)
        self.assertEqual(self.obj, self.ns.private.obj)
        self.assertEqual(self.obj, self.ns.nonprivate.obj)

class TestBasic(TestCase):
    def setUp(self):
        self.test_obj = TestObject()
        self.test_obj2 = ComplexTestObject()
        self.test_ns = Namespace(self.test_obj)

    def test_subobject_with_attr(self):
        self.assertEqual(
            ['_private_method'],
            self.test_ns.subobjects.with_attr('test_attr').keys())

    def test_properties(self):
        self.assertEqual(self.test_ns.properties.values(),
                         [TestObject._some_private_property])

    def test_locals(self):
        test_ns2 = Namespace(self.test_obj2)
        tmp = test_ns2.locals
        self.assertEqual(tmp.keys(), ['my_class_variable'])

    def test_keys(self):
        diff = list(set(self.test_ns.keys()) - set(dir(self.test_obj)))
        self.assertFalse(diff)

    def test_clean(self):
        self.assertTrue('__class__' not in self.test_ns.nonprivate)
        self.assertTrue('_private_method' not in self.test_ns.nonprivate)

    def test_methods(self):
        self.assertTrue([self.test_obj._private_method],
                        self.test_ns.methods.values())

    def test_startswith(self):
        self.assertEqual(self.test_ns.startswith('pub').keys(),
                         ['public_static_method'])

    def test_private(self):
        diff = set(self.test_ns.keys()) - set(self.test_ns.private.keys())
        self.assertEqual(diff, set(['class_variable','public_static_method']))

    def test_functions(self):
        self.assertTrue([self.test_obj.public_static_method],
                        self.test_ns.functions.values())

    def test_class_variables(self):
        self.assertTrue(['class_variable'],
                        self.test_ns.class_variables.keys())

if __name__=='__main__':
    main()
