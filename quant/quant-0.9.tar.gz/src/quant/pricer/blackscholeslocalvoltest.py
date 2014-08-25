import unittest
from quant.pricer.basetest import PricerTestCase
from quant.testunit import VOLATILITY_MEDIUM
from quant.testunit import VOLATILITY_LOW
from quant.testunit import VOLATILITY_HIGH
from quant.testunit import VOLATILITY_ZERO
from quant.pricer.simple import EuropeanBlackScholesLocalVol

def suite():
    suites = [
        unittest.makeSuite(TestCallStrike9),
        #unittest.makeSuite(TestCallStrike10),
        #unittest.makeSuite(TestCallStrike11),
        #unittest.makeSuite(TestCallStrike12),
    ]
    return unittest.TestSuite(suites)

# Start with the market prices of options with different strikes and different
# expiry times, and work out volatility function sigma(underlying price, current time)
# such that when you price the European option with Monte Carlo you get back what you 
# started with.

#from quant.pricer.simple import EuropeanBlackScholes
class BlackScholesLocalVolTestCase(PricerTestCase):
    #pricerClass = EuropeanBlackScholesLocalVol
    DECIMALS = 3
    pricerClass = EuropeanBlackScholesLocalVol
    expectedValue = 1

    def setUp(self):
        self.pricer = self.pricerClass(
            image=self.registry.images.get(1)
        )


class TestCallStrike9(BlackScholesLocalVolTestCase):

# Need a book with local volatility price process, need to get volatility surface from price process and use it in the contract type.

    expectedValue = 2.416
    expectedDelta = 0.678
    expectedGamma = 0.072







#class TestCallStrike10(BlackScholesLocalVolTestCase):
#    expectedValue = 1.935
#    expectedDelta = 0.597
#    expectedGamma = 0.079


