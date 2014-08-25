import unittest
import quant.priceprocess.simpletest

def suite():
    suites = [
        quant.priceprocess.simpletest.suite(),
    ]
    return unittest.TestSuite(suites)

