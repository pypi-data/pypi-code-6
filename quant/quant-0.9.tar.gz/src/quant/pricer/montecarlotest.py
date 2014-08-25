import unittest
import sys

import quant.pricer.basetest as basetest
from quant.pricer.basetest import ignoreTest
from quant.pricer.simple import EuropeanMonteCarlo
from quant.pricer.simple import AmericanMonteCarlo


def suite():
    return unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

# Todo: Configurable pathCount (tests want low value, sites want high value).


class TestEuropeanCall(basetest.MonteCarloPricerTestCase):

    pricerClass = EuropeanMonteCarlo

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 2.416
    expectedDelta = 0.677
    expectedGamma = 0.07


class TestEuropeanPut(basetest.MonteCarloPricerTestCase):

    pricerClass = EuropeanMonteCarlo
    isPut = True

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 1.416


@ignoreTest
class TestAmericanCall(basetest.MonteCarloPricerTestCase):

    pricerClass = AmericanMonteCarlo

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 2.416


@ignoreTest
class TestAmericanPut(basetest.MonteCarloPricerTestCase):

    pricerClass = AmericanMonteCarlo
    isPut = True

    strikePrice = 9
    lastPrice = 10
    actualHistoricalVolatility = 50
    expectedValue = 1.416


