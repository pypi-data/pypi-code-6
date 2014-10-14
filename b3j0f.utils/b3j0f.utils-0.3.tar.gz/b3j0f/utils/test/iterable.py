#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main

from b3j0f.utils.ut import UTCase
from b3j0f.utils.iterable import first, ensureiterable, isiterable
from b3j0f.utils.version import basestring


class EnsureIterableTest(UTCase):

    def test_list(self):

        l = []
        itererable = ensureiterable(l)
        self.assertEqual(itererable, l)

    def test_dict(self):

        l = []
        iterable = ensureiterable(l, iterable=dict)
        self.assertTrue(isinstance(iterable, dict))
        self.assertFalse(iterable)

    def test_notallowed(self):

        l = ""
        iterable = ensureiterable(l, notallowed=basestring)
        self.assertTrue(iterable)


class IsIterable(UTCase):

    def test_iterable(self):
        """
        Test an iterable value
        """

        self.assertTrue(isiterable([]))

    def test_notallowed(self):
        """
        Test iterable and not allowed types
        """

        self.assertFalse(isiterable([], notallowed=list))

    def test_notalloweds(self):
        """
        Test iterable with a tuple of notallowed types
        """

        self.assertFalse(isiterable([], notallowed=(list, basestring)))

    def test_not_iterable(self):
        """
        Test not iterable element
        """

        self.assertFalse(isiterable(None))


class First(UTCase):

    def test_empty(self):
        """
        Test empty iterable
        """

        self.assertIs(first([]), None)

    def test_first(self):
        """
        Test first element in an iterable
        """

        value = 'value'
        iterable = [value]

        self.assertIs(first(iterable), value)

    def test_default(self):
        """
        Test default value
        """

        default = 'default'

        self.assertIs(first([], default), default)

    def test_notiterable(self):
        """
        Test not iterable
        """

        self.assertRaises(TypeError, first, True)

if __name__ == '__main__':
    main()
