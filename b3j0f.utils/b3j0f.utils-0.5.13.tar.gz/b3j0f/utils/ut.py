# -*- coding: utf-8 -*-

"""
Unit tests tools.
"""

from unittest import TestCase

from b3j0f.utils.version import PY26


class UTCase(TestCase):
    """
    Class which enrichs TestCase with python version compatibilities
    """

    def __init__(self, *args, **kwargs):

        super(UTCase, self).__init__(*args, **kwargs)

        if PY26:  # if python version is 2.6
            self.assertIs = lambda a, b, *args, **kwargs: self.assertTrue(
                a is b, *args, **kwargs)
            self.assertIsNot = lambda a, b, *args, **kwargs: self.assertFalse(
                a is b, *args, **kwargs)
            self.assertIsNone = lambda a, *args, **kwargs: self.assertIs(
                a, None, *args, **kwargs)
            self.assertIsNotNone = lambda a, *args, **kwargs: self.assertIsNot(
                a, None, *args, **kwargs)
            self.assertIn = lambda a, b, *args, **kwargs: self.assertTrue(
                a in b, *args, **kwargs)
            self.assertNotIn = lambda a, b, *args, **kwargs: self.assertTrue(
                a not in b, *args, **kwargs)
            self.assertLess = lambda a, b, *args, **kwargs: self.assertTrue(
                a < b, *args, **kwargs)
            self.assertGreater = lambda a, b, *args, **kwargs: self.assertTrue(
                a > b, *args, **kwargs)
            self.assertGreaterEqual = lambda a, b, *args, **kwargs: \
                self.assertTrue(a >= b, *args, **kwargs)
            self.assertLessEqual = lambda a, b, *args, **kwargs: \
                self.assertTrue(a <= b, *args, **kwargs)
            self.assertRegexpMatches = lambda s, r, *args, **kwargs: \
                self.assertTrue(r.search(s), *args, **kwargs)
            self.assertNotRegexpMatches = lambda s, r, *args, **kwargs: \
                self.assertTrue(not r.search(s), *args, **kwargs)
            self.assertItemsEqual = lambda a, b, *args, **kwargs: \
                self.assertEqual(sorted(a), sorted(b), *args, **kwargs)

            def subset(a, b):
                result = True
                for k in a:
                    result = k in b and a[k] == b[k]
                    if not result:
                        break
                return result
            self.assertDictContainsSubset = lambda a, b, *args, **kwargs: \
                self.assertTrue(subset(a, b), *args, **kwargs)
