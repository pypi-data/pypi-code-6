class MarketData(object):

    def __init__(self, dataService, name):
        self.dataService = dataService
        self.name = name

    def getLastPrice(self, market):
        return self.getDataService().getLastPrice(market=market)

    def getActualHistoricalVolatility(self, market=None):
        return self.getDataService().getActualHistoricalVolatility(market=market)

    def getNowTime(self):
        return self.getDataService().getNowTime()

    def getPeriodsUntil(self, market):
        return self.getDataService().getPeriodsUntil(market=market)

    def getDataService(self):
        if self.dataService == 'test':
            return StubMarketDataService()
        else:
            raise Exception, "Data service not supported: %s" % self.dataService

    def getPriceProcess(self):
        return self.getDataService().getPriceProcess()

class AbstractMarketDataService(object):

    def getLastPrice(self, market):
        raise Exception, "Method not implemented."

    def getActualHistoricalVolatility(self, market=None):
        raise Exception, "Method not implemented."

    def getPriceProcess(self):
        raise Exception, "Method not implemented."
        return self.getDataService().getPriceProcess()

class StubMarketDataService(AbstractMarketDataService):

    data = [
        {
            'market': '2010-10-06',
            'current': 10,
            'actualHistoricalVolatility': 1,
        },
        {
            'market': '2010-11-06',
            'current': 12,
            'actualHistoricalVolatility': 1,
        },
        {
            'market': '2010-12-06',
            'current': 9,
            'actualHistoricalVolatility': 1,
        },
        {
            'market': '2011-01-06',
            'current': 10,
            'actualHistoricalVolatility': 1,
        },

    ]

    def getItem(self, market):
        for item in self.data:
            if item['market'] == market:
                return item
        msg = "Period not found in data: %s" % market
        raise Exception, msg

    def getLastPrice(self, market):
        return self.getItem(market)['current']

    def getActualHistoricalVolatility(self, market=None):
        return 50

    def getNowTime(self):
        return '2010-01-06 00:00:00'

    def getPriceProcess(self):
        return BlackScholesProcess()

class BlackScholesProcess(object):
    pass
