# -*- coding: utf-8 -*-
import unittest2 as unittest
# from Products.CMFCore.utils import getToolByName

from .testing import CALENDAR_INTEGRATION


class TestSetup(unittest.TestCase):
    layer = CALENDAR_INTEGRATION

    def test_catalog_metadata(self):
        self.assertTrue(2 + 2, 4)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
