""" test_classproperty:
      tests for goulash.classproperty
"""
import unittest

from goulash.classproperty import classproperty

class testing(object):
    @classproperty
    def test(kls): return 3

class TestClassProperty(unittest.TestCase):
    def test_classproperty(self):
        self.assertEqual(testing.test, 3)
