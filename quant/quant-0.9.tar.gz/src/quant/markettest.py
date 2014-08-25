from quant.dom.testunit import TestCase
from quant.market import BlackScholesProcess
import unittest

def suite():
    suites = [
        unittest.makeSuite(TestMarketData),
    ]
    return unittest.TestSuite(suites)

class TestMarketData(TestCase):

    marketDataService = 'test'
    marketName = 'CL'
    marketMarket = '2011-01-06'

    expectedNowTime = '2010-01-06 00:00:00'
    expectedLastPrices = [10, 12, 9, 10]
    expectedVolatilities = [50, 50, 50, 50]
    expectedMarkets = ['2010-10-06', '2010-11-06', '2010-12-06', '2011-01-06']
    expectedPriceProcessClass = BlackScholesProcess

    def setUp(self):
        from quant.market import MarketData
        self.market = MarketData(
            dataService=self.marketDataService,
            name=self.marketName,
        )

    def test_getLastPrice(self):
        for i in range(len(self.expectedMarkets)):
            market = self.expectedMarkets[i]
            lastPrice = self.market.getLastPrice(market=market)
            self.assertEqual(lastPrice, self.expectedLastPrices[i])

    def test_getActualHistoricalVolatility(self):
        for i in range(len(self.expectedMarkets)):
            market = self.expectedMarkets[i]
            actualHistoricalVolatility = self.market.getActualHistoricalVolatility(market=market) 
            self.assertEqual(actualHistoricalVolatility, self.expectedVolatilities[i])

    def test_getNowTime(self):
        self.assertEqual(self.market.getNowTime(), self.expectedNowTime)

    def test_getPriceProcess(self):
        self.assertEqual(type(self.market.getPriceProcess()), self.expectedPriceProcessClass)

