#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main

from time import sleep

from b3j0f.utils.ut import UTCase
from b3j0f.utils.property import (
    get_properties, put_properties, del_properties, get_local_properties,
    unify, OrderedDict, get_local_property, get_property, get_first_property,
    setdefault, put_property
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
        put_properties(elt, properties=properties)

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
        put_properties(A, properties=properties)

        properties = get_properties(B)
        self.assertEqual(len(properties), 1)
        self.assertIn(A, properties)

        local_properties = get_local_properties(B)
        self.assertEqual(len(local_properties), 0)

        properties = dict((str(i), i) for i in range(count))
        put_properties(B, properties=properties)

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
        put_properties(A, properties=properties)

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

        #self._assert_properties(a.a)

        count = 10

        properties = dict((str(i), i) for i in range(count))
        put_properties(A.a, properties=properties, ctx=A)

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

    def test_dict(self):

        elt = {}

        self.assertRaises(TypeError, get_properties, elt)

    def test_list(self):

        elt = []

        self.assertRaises(TypeError, get_properties, elt)


class TTLTest(UTCase):

    def setUp(self):
        pass

    def tearDown(self):

        del_properties(self)

    def test_zero(self):

        put_property(self, ttl=0, key='name', value=1)

        sleep(0.1)

        properties = get_local_properties(self)

        self.assertFalse(properties)

    def test_100(self):

        ttl = 0.1

        put_property(self, ttl=ttl, key='name', value=1)

        properties = get_local_properties(self)

        self.assertTrue(properties)

        sleep(ttl + 0.2)

        properties = get_local_properties(self)

        self.assertFalse(properties)


class OneTest(UTCase):
    """
    UT for get_local_property and get_first_property
    """

    def tearDown(self):

        del_properties(self)

    def test_first_none(self):

        _property = get_first_property(self, 'a', 2)

        self.assertEqual(_property, 2)

    def test_first(self):

        put_property(self, key='a', value=1)

        _property = get_first_property(self, 'a', 2)

        self.assertEqual(_property, 1)

    def test_none_local(self):

        local_property = get_local_property(self, 'a', 2)

        self.assertEqual(local_property, 2)

    def test_local(self):

        put_property(self, key='a', value=1)

        local_property = get_local_property(self, 'a', 2)

        self.assertEqual(local_property, 1)

    def test_none(self):

        _property = get_property(self, 'a')

        self.assertFalse(_property)

    def test_property(self):

        put_property(self, key='a', value=1)

        _property = get_property(self, 'a')

        self.assertEqual(_property[self], 1)


class UnifyTest(UTCase):

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


class SetDefaultTest(UTCase):
    """
    Test setdefault function
    """

    def setUp(self):

        self.key = 'test'

        self.new_value = 2

    def tearDown(self):

        del_properties(self)

    def test_exists(self):
        """
        Test with an existing property
        """

        put_properties(self, properties={self.key: self.new_value + 1})

        value = setdefault(self, self.key, self.new_value)

        self.assertNotEqual(value, self.new_value)

    def test_new(self):
        """
        Test on a missing property
        """

        value = setdefault(self, self.key, self.new_value)

        self.assertEqual(value, self.new_value)


if __name__ == '__main__':
    main()
