import abc
import unittest
import unittest.case
import datetime

from quant.dom.testunit import TestCase


def ignoreTest(*args):
    return unittest.TestCase

# def skipBaseTestCase(testCaseClass):
#     raise Exception(testCaseClass)
#     if testCaseClass.__name__.endswith('TestCase'):
#         return unittest.TestCase
#     else:
#         return testCaseClass

# class skipBaseTestCase(object):
#
#     def __init__(self, *args, **kwds):
#         self.args = args
#         self.kwds = kwds
#
#     def __call__(self, callable):
#         if callable().__name__.endswith('TestCase'):
#             raise Exception("Blah")
#         return cls


class PricerTestCase(TestCase):

    __metaclass__ = abc.ABCMeta

    DECIMALS = 4

    pricerClass = None
    isPut = False

    strikePrice = 10
    lastPrice = 10
    actualHistoricalVolatility = 50
    annualRiskFreeRate = 0
    tolerance = 1e-8
    nowTime = datetime.datetime(2010, 1, 1)
    expiration = datetime.datetime(2011, 1, 1)
    daysPerYear = 365

    expectedExceptionClass = None

    expectedValue = 0
    expectedDelta = None
    expectedGamma = None
    expectedVega = None

    def setUp(self):
        self.assertTrue(self.pricerClass, "Pricer class missing on %s." % self.__class__.__name__)
            
        self.pricer = self.pricerClass(
            strikePrice=self.strikePrice,
            lastPrice=self.lastPrice,
            actualHistoricalVolatility=self.actualHistoricalVolatility,
            durationYears=float((self.expiration-self.nowTime).days) / self.daysPerYear,
            annualRiskFreeRate=self.annualRiskFreeRate,
            isPut=self.isPut,
        )

    def testPricerValuation(self):
        self.assertExpectedValueDeltaGamma(
            expectedValue=self.expectedValue,
            expectedDelta=self.expectedDelta,
            expectedGamma=self.expectedGamma)

    def assertExpectedValueDeltaGamma(self, expectedValue, expectedDelta, expectedGamma):
        if self.__class__ == PricerTestCase:
            self.skipTest("Abstract test case...")
        if self.expectedExceptionClass:
            self.assertRaises(self.expectedExceptionClass, self.pricer.calcValue)
            return
        # Check option value.
        estimatedValue = self.pricer.calcValue()
        roundedValue = round(estimatedValue, self.DECIMALS)
        expectedValue = round(self.expectedValue, self.DECIMALS)
        msg = "Value: %s  Expected: %s  Strike: %s  Current: %s  Volatility: %s  Rate: %s" % (roundedValue, expectedValue, self.strikePrice, self.lastPrice, self.actualHistoricalVolatility, self.annualRiskFreeRate)
        self.assertEqual(roundedValue, expectedValue, msg)

        # Check option delta.
        if self.expectedDelta == None:
            return
        estimatedDelta = self.pricer.calcDelta(estimatedValue)
        roundedDelta = round(estimatedDelta, self.DECIMALS)
        expectedDelta = round(self.expectedDelta, self.DECIMALS)
        msg = "Delta: %s  Expected: %s  Strike: %s  Current: %s  Volatility: %s  Rate: %s" % (roundedDelta, expectedDelta, self.strikePrice, self.lastPrice, self.actualHistoricalVolatility, self.annualRiskFreeRate)
        self.assertEqual(roundedDelta, expectedDelta, msg)

        # Check option gamma.
        if self.expectedGamma == None:
            return
        estimatedGamma = self.pricer.calcGamma(estimatedValue, estimatedDelta)
        roundedGamma = round(estimatedGamma, self.DECIMALS)
        expectedGamma = round(self.expectedGamma, self.DECIMALS)
        msg = "Gamma: %s  Expected: %s  Strike: %s  Current: %s  Volatility: %s  Rate: %s" % (roundedGamma, expectedGamma, self.strikePrice, self.lastPrice, self.actualHistoricalVolatility, self.annualRiskFreeRate)
        self.assertEqual(roundedGamma, expectedGamma, msg)


class MonteCarloPricerTestCase(PricerTestCase):

    DECIMALS = 1


