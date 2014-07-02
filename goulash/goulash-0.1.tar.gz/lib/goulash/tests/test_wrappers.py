""" test_wrappers:

      tests for goulash.wrappers
"""

import unittest

from goulash.wrappers import JSONWrapper, DumbWrapper

class TestWrappers(unittest.TestCase):
    def setUp(self):
        self.data = dict(foo='bar')
        self.jwrapper = JSONWrapper(self.data)
        self.dwrapper = DumbWrapper(self.data)

    def test_json_wrapper_data(self):
        self.assertEqual(self.jwrapper.foo, 'bar')

    def test_json_wrapper_default(self):
        self.jwrapper.test=1
        self.assertEqual(self.jwrapper.test, 1)
