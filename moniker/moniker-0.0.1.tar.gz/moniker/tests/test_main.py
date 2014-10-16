# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import sys

from unittest import TestCase

from nose.tools import *

sys.path.insert(0, os.path.abspath('..'))

class TestMain(TestCase):

    def test_main(self):
        pass


if __name__ == '__main__':
    unittest.main()
