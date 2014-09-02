#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""All yatel tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import unittest

from yatel.tests import (
    core,
    test_db,
    test_dom,
    test_db,
    test_dom,
    test_stats,
    test_typeconv,
    test_qbj,
    test_cluster,
    test_yio,
    test_weight,
    test_server,
    test_client,
    test_etl
)


#===============================================================================
# FUNCTIONS
#===============================================================================

def run_tests(verbosity=1):

    def collect(cls):
        collected = set()
        for testcls in cls.subclasses():
            collected.add(testcls)
            collected.update(collect(testcls))
        return collected

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    runner = unittest.runner.TextTestRunner(verbosity=verbosity)
    for testcase in collect(core.YatelTestCase):
        tests = loader.loadTestsFromTestCase(testcase)
        if tests.countTestCases():
                suite.addTests(tests)
    return runner.run(suite)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
