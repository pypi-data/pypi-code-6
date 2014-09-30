#coding: utf-8

import unittest

from bdd_testcase import DjangoBDDTestCase


def suite():
    suite = unittest.TestSuite()
    for func_name in DjangoBDDTestCase.__feature_handlers:
        suite.addTest(DjangoBDDTestCase(func_name))
    return suite
