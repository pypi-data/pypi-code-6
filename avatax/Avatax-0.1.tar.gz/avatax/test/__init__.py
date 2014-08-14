# -*- coding: utf-8 -*-
"""
    __init__

    Collect all Tests

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import unittest

from .test_api import TestAPI


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestAPI)
    )
    return test_suite
