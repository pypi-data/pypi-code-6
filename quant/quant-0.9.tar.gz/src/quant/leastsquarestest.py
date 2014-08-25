import unittest

from quantdsl.test import TestLeastSquares


def suite():
    suites = [
        unittest.makeSuite(TestLeastSquares),
    ]
    return unittest.TestSuite(suites)


