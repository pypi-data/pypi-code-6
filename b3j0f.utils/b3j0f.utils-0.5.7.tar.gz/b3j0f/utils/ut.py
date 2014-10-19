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
            self.assertIs = lambda x, y, *args, **kwargs: self.assertTrue(
                x is y, *args, **kwargs)
            self.assertIsNot = lambda x, y, *args, **kwargs: self.assertFalse(
                x is y, *args, **kwargs)
            self.assertIsNone = lambda x, *args, **kwargs: self.assertIs(
                x, None, *args, **kwargs)
            self.assertIsNotNone = lambda x, *args, **kwargs: self.assertIsNot(
                x, None, *args, **kwargs)
            self.assertIn = lambda x, y, *args, **kwargs: self.assertTrue(
                x in y, *args, **kwargs)
            self.assertNotIn = lambda x, y, *args, **kwargs: self.assertTrue(
                x not in y, *args, **kwargs)
