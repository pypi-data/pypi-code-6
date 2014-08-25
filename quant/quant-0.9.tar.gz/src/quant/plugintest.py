import unittest
import quant.plugin.basetest

def suite():
    suites = [
        quant.plugin.basetest.suite(),
    ]
    return unittest.TestSuite(suites)

