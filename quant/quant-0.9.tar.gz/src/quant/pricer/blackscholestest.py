import unittest
from quant.pricer.basetest import PricerTestCase
from quant.testunit import VOLATILITY_MEDIUM
from quant.testunit import VOLATILITY_LOW
from quant.testunit import VOLATILITY_HIGH
from quant.testunit import VOLATILITY_ZERO
from quant.pricer.simple import EuropeanBlackScholes

def suite():
    suites = [
        unittest.makeSuite(TestBlackScholesCall),
        unittest.makeSuite(TestBlackScholesCallOnMoney),
        unittest.makeSuite(TestBlackScholesCallInMoney),
        unittest.makeSuite(TestBlackScholesCallOutMoney),
        unittest.makeSuite(TestBlackScholesCallLowRate),
        unittest.makeSuite(TestBlackScholesCallHighRate),
        unittest.makeSuite(TestBlackScholesPut),
        unittest.makeSuite(TestBlackScholesPutOnMoney),
        unittest.makeSuite(TestBlackScholesPutOutMoney),
        unittest.makeSuite(TestBlackScholesPutInMoney),
        unittest.makeSuite(TestBlackScholesPutLowRate),
        unittest.makeSuite(TestBlackScholesPutHighRate),
    ]
    return unittest.TestSuite(suites)


class BlackScholesTestCase(PricerTestCase):

    pricerClass = EuropeanBlackScholes
    strikePrice = 9.0

class BlackScholesCallTestCase(BlackScholesTestCase):
    pass

class TestBlackScholesCall(BlackScholesCallTestCase):
    lastPrice = 10.0
    expectedValue = 2.416

class TestBlackScholesCallOnMoney(BlackScholesCallTestCase):
    lastPrice = 9.0
    expectedValue = 1.7767

class TestBlackScholesCallInMoney(BlackScholesCallTestCase):
    lastPrice = 20.0
    expectedValue = 11.1534

class TestBlackScholesCallOutMoney(BlackScholesCallTestCase):
    lastPrice = 3.0
    expectedValue = 0.0125

class TestBlackScholesCallLowRate(BlackScholesCallTestCase):
    lastPrice = 10.0
    annualRiskFreeRate = 1.0
    expectedValue = 2.4597

class TestBlackScholesCallHighRate(BlackScholesCallTestCase):
    lastPrice = 10.0
    annualRiskFreeRate = 10.0
    expectedValue = 2.8644

class BlackScholesPutTestCase(BlackScholesTestCase):
    isPut = True

class TestBlackScholesPut(BlackScholesPutTestCase):
    lastPrice = 10.0
    expectedValue = 1.416

class TestBlackScholesPutOnMoney(BlackScholesPutTestCase):
    lastPrice = 9.0
    expectedValue = 1.7767

class TestBlackScholesPutOutMoney(BlackScholesPutTestCase):
    lastPrice = 20.0
    expectedValue = 0.1534

class TestBlackScholesPutInMoney(BlackScholesPutTestCase):
    lastPrice = 3.0
    expectedValue = 6.0125

class TestBlackScholesPutLowRate(BlackScholesPutTestCase):
    lastPrice = 10.0
    annualRiskFreeRate = 1.0
    expectedValue = 1.3702

class TestBlackScholesPutHighRate(BlackScholesPutTestCase):
    lastPrice = 10.0
    annualRiskFreeRate = 10.0
    expectedValue = 1.0079

