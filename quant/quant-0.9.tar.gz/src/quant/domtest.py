import unittest
import quant.testunit
import quant.dom.buildertest
import quant.dom.booktest
import quant.dom.markettest
import quant.dom.resulttest

def suite():
    suites = [
        quant.dom.buildertest.suite(),
        quant.dom.booktest.suite(),
        quant.dom.markettest.suite(),
        quant.dom.resulttest.suite(),
    ]
    return unittest.TestSuite(suites)

