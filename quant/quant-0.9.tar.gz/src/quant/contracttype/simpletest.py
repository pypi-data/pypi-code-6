import unittest
from quant.dom.testunit import TestCase
from quant.testunit import VOLATILITY_MEDIUM
from quant.testunit import VOLATILITY_LOW
from quant.testunit import VOLATILITY_HIGH
from quant.testunit import VOLATILITY_ZERO

def suite():
    suites = [
    ]
    return unittest.TestSuite(suites)


class DerivativesContractTestCase(TestCase):

    contractVolume = 10
    contractStrikePrice = 10
    contractMarket = '2011-01-06'
    contractIsPut = False

    marketDataService = 'test'
    marketName = 'CL' # Oil market. 

    expectedMarketLastPrice = 10
    expectedMarketVolatility = 50
    expectedContractValue = None

    def setUp(self):
        super(DerivativesContractTestCase, self).setUp()
        self.contract = self.createContract()

    def tearDown(self):
        if self.contract:
            self.contract.delete()
        super(DerivativesContractTestCase, self).tearDown()

    def createContract(self, **kwds):
        return self.getContractsRegister().create(
            volume=self.contractVolume,
            strikePrice=self.contractStrikePrice,
            market=self.contractMarket,
            isPut=self.contractIsPut,
            marketDataService=self.marketDataService,
            marketName=self.marketName,
            **kwds
        )

    def getContractsRegister(self):
        raise Exception("Method not implemented.")

    def test_evaluate(self):
        self.failUnlessEqual(self.contract.market.calcLastPrice(market=self.contractExpiryTime), self.expectedMarketLastPrice)
        self.failUnlessEqual(self.contract.market.getActualHistoricalVolatility(market=self.contractExpiryTime), self.expectedMarketVolatility)
        self.contract.evaluate()
        contractValue = round(self.contract.value, 4)
        msg = self.getEvaluateErrorMsg(contractValue)
        self.failUnlessEqual(contractValue, self.expectedContractValue, msg)

    def getEvaluateErrorMsg(self, contractValue):
        msg = "Value: %s  Expected: %s  Volume: %s  Strike: %s  Current: %s  Volatility: %s" % (contractValue, self.expectedContractValue, self.contract.volume, self.contract.strikePrice, self.contract.market.calcLastPrice(market=self.contractExpiryTime), self.contract.market.getActualHistoricalVolatility(market=self.contractExpiryTime))
        return msg


class AmericanTestCase(DerivativesContractTestCase):

    def getContractsRegister(self):
        return self.registry.americans


class BinaryTestCase(DerivativesContractTestCase):

    def getContractsRegister(self):
        return self.registry.binarys


class DslTestCase(DerivativesContractTestCase):

    def getContractsRegister(self):
        return self.registry.dsls


class EuropeanTestCase(DerivativesContractTestCase):

    def getContractsRegister(self):
        return self.registry.europeans


class FuturesTestCase(DerivativesContractTestCase):

    def getContractsRegister(self):
        return self.registry.futures


