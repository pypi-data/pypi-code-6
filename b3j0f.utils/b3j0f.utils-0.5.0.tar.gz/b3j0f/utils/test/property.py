#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main

from b3j0f.utils.ut import UTCase
from b3j0f.utils.property import (
    get_properties, put_properties, del_properties, get_local_properties,
    unify, OrderedDict
)


class PropertyTest(UTCase):

    def setUp(self):
        pass

    def _assert_properties(self, elt, count=10):

        properties = get_properties(elt)
        self.assertFalse(properties)
        local_properties = get_local_properties(elt)
        self.assertFalse(local_properties)

        properties = dict((str(i), i) for i in range(count))
        put_properties(elt, **properties)

        local_properties = get_local_properties(elt)
        properties = get_properties(elt)

        self.assertEqual(len(properties), 1)
        self.assertIn(elt, properties)

        self.assertEqual(len(properties[elt]), count)
        self.assertEqual(len(local_properties), 10)

        for i in range(count):
            self.assertEqual(properties[elt][str(i)], i)
            self.assertEqual(local_properties[str(i)], i)

        properties = get_properties(elt, '0')
        self.assertEqual(len(properties), 1)
        self.assertIn('0', properties[elt])

        local_properties = get_local_properties(elt, '0')
        self.assertEqual(len(local_properties), 1)
        self.assertIn('0', local_properties)

        del_properties(elt, '0')

        properties = get_properties(elt)
        self.assertEqual(len(properties), 1)
        self.assertEqual(len(properties[elt]), count - 1)

        local_properties = get_local_properties(elt)
        self.assertEqual(len(local_properties), 9)

        for i in range(1, count):
            self.assertEqual(properties[elt][str(i)], i)
            self.assertEqual(local_properties[str(i)], i)

        del_properties(elt)
        properties = get_properties(elt)
        self.assertFalse(properties)
        local_properties = get_local_properties(elt)
        self.assertFalse(local_properties)

    def test_builtin(self):
        """
        Test lookup of builtin
        """

        self._assert_properties(min)

    def test_object(self):

        self._assert_properties(1)

    def test_none(self):

        self._assert_properties(None)

    def test_lambda(self):

        self._assert_properties(lambda: None)

    def test_function(self):

        def a():
            pass

        self._assert_properties(a)

    def test_class(self):

        class A(object):
            pass

        self._assert_properties(A)

        class B(A):
            pass

        count = 10

        properties = dict((str(i), i) for i in range(count))
        put_properties(A, **properties)

        properties = get_properties(B)
        self.assertEqual(len(properties), 1)
        self.assertIn(A, properties)

        local_properties = get_local_properties(B)
        self.assertEqual(len(local_properties), 0)

        properties = dict((str(i), i) for i in range(count))
        put_properties(B, **properties)

        properties = get_properties(B)
        self.assertEqual(len(properties), 2)
        self.assertIn(A, properties)
        self.assertIn(B, properties)

        local_properties = get_local_properties(B)
        self.assertEqual(len(local_properties), 10)

    def test_instance(self):

        class A:
            pass

        a = A()

        self._assert_properties(a)

        count = 10

        properties = dict((str(i), i) for i in range(count))
        put_properties(A, **properties)

        properties = get_properties(a)
        self.assertEqual(len(properties), 1)
        self.assertIn(A, properties)

        local_properties = get_local_properties(a)
        self.assertEqual(len(local_properties), 0)

    def test_namespace(self):

        class A:
            pass

        self._assert_properties(A)

    def test_method(self):

        class A:
            def a(self):
                pass

        self._assert_properties(A.a)

    def test_bound_method(self):

        class A(object):
            def a(self):
                pass

        a = A()

        self._assert_properties(a.a)

        count = 10

        properties = dict((str(i), i) for i in range(count))
        put_properties(A.a, **properties)

        properties = get_properties(a.a)
        self.assertEqual(len(properties), 1)
        self.assertIn(A.a, properties)

        local_properties = get_local_properties(a.a)
        self.assertEqual(len(local_properties), 0)

    def test_module(self):

        import b3j0f

        self._assert_properties(b3j0f)

    def test_property_module(self):

        import b3j0f.utils.property

        self._assert_properties(b3j0f.utils.property)


class UnifyTest(UTCase):

    def setUp(self):
        pass

    def test_empty(self):

        properties = {}

        unified_properties = unify(properties)

        self.assertFalse(unified_properties)

    def test_one_value(self):

        properties = {1: {1: 1}}

        unified_properties = unify(properties)

        self.assertIn(1, unified_properties)
        self.assertEqual(unified_properties[1], 1)

    def test_values(self):

        count = 10

        properties = OrderedDict()

        for i in range(count):
            properties[i] = OrderedDict()
            for j in range(i + 1):
                properties[i][j] = j

        unified_properties = unify(properties)

        self.assertEqual(len(unified_properties), count)
        for i in range(count):
            self.assertEqual(unified_properties[i], i)


if __name__ == '__main__':
    main()
