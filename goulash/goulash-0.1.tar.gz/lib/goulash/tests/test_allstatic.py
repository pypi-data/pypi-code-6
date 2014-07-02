""" goulash.tests.test_allstatic
"""

import unittest

from goulash.allstatic import AllStaticMethods


class TestAllStatic(unittest.TestCase):

    def test_basic(self):
        class Testing(object):
            __metaclass__ = AllStaticMethods
            def foo(): return 'foo'
        self.assertEqual(Testing.foo(),'foo')
