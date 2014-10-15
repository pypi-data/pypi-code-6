#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main

from b3j0f.utils.ut import UTCase
from b3j0f.utils.property import get_properties, put_properties, del_properties


class PropertyTest(UTCase):

    def setUp(self):
        pass

    def _assert_properties(self, elt, count=10):

        properties = get_properties(elt)
        self.assertFalse(properties)

        properties = dict((str(i), i) for i in range(count))
        put_properties(elt, **properties)

        properties = get_properties(elt)
        self.assertEqual(len(properties), 1)
        self.assertIn(elt, properties)

        self.assertEqual(
            len(properties[elt]), count)
        for i in range(count):
            self.assertEqual(properties[elt][str(i)], i)

        properties = get_properties(elt, '0')
        self.assertEqual(len(properties), 1)
        self.assertIn('0', properties[elt])

        del_properties(elt, '0')

        properties = get_properties(elt)
        self.assertEqual(len(properties), 1)
        self.assertEqual(len(properties[elt]), count - 1)
        for i in range(1, count):
            self.assertEqual(properties[elt][str(i)], i)

        del_properties(elt)
        properties = get_properties(elt)
        self.assertFalse(properties)

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

    def test_module(self):

        import b3j0f

        self._assert_properties(b3j0f)

    def test_property_module(self):

        import b3j0f.utils.property

        self._assert_properties(b3j0f.utils.property)


if __name__ == '__main__':
    main()
