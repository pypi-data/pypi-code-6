import unittest
from quant.pricer.basetest import PricerTestCase
from quant.pricer.simple import EuropeanBinomialTree
from quant.pricer.simple import AmericanBinomialTree

def suite():
    suites = [
        unittest.makeSuite(TestEuropeanCall),
        unittest.makeSuite(TestEuropeanPut),
        unittest.makeSuite(TestAmericanCall),
        unittest.makeSuite(TestAmericanPut),
    ]
    return unittest.TestSuite(suites)


class BinomialTreeTestCase(PricerTestCase):

    DECIMALS = 3


class TestEuropeanCall(BinomialTreeTestCase):

    pricerClass = EuropeanBinomialTree

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 2.416


class TestEuropeanPut(BinomialTreeTestCase):

    pricerClass = EuropeanBinomialTree
    isPut = True

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 1.416


class TestAmericanCall(BinomialTreeTestCase):

    pricerClass = AmericanBinomialTree

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 2.416


class TestAmericanPut(BinomialTreeTestCase):

    pricerClass = AmericanBinomialTree
    isPut = True

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 1.416

