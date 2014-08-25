import scipy
import math

class PriceProcess(object): pass

class SimplePriceProcess(PriceProcess):

    daysPerYear = 365

    def getDurationYears(self, start, end):
        duration = end - start
        return float(duration.days) / self.daysPerYear

    def getMetricValue(self, metricName, market, observationTime):
        calcMethodName = self.getCalcMethodName(metricName)
        try:
            calcMethod = getattr(self, calcMethodName)
        except AttributeError:
            try:
                calcMethod = getattr(market, calcMethodName)
            except AttributeError:
                msg = "Metric '%s' not supported" % metricName
                msg += " on '%s' price process" % self.__class__.__name__
                msg += " or '%s' market type" % market.__class__.__name__
                msg += " (method '%s' not found)." % calcMethodName
                raise Exception, msg
            else:
                return calcMethod(observationTime)
        else:
            return calcMethod(market, observationTime)

    def getCalcMethodName(self, metricName):
        return 'calc'+''.join([i.capitalize() for i in metricName.split('-')])


class BlackScholesVolatility(SimplePriceProcess):

    def calcActualHistoricalVolatility(self, market, observationTime):
        priceHistory = market.getPriceHistory(observationTime=observationTime)
        prices = scipy.array([i.value for i in priceHistory])
        dates = [i.observationTime for i in priceHistory]
        volatility = 100 * prices.std() / prices.mean()
        duration = max(dates) - min(dates)
        years = (duration.days) / 365.0 # Assumes zero seconds.
        if years == 0:
            raise Exception, "Can't calculate volatility for price series with zero duration: %s" % (priceHistory)
        return float(volatility) / math.sqrt(years)


class LocalVolatility(SimplePriceProcess): pass

    #def calcLocalVolatilitySurface(self):
    #    pass


class StochasticVolatilityHeston(SimplePriceProcess): pass

class StochasticVolatilitySABR(SimplePriceProcess): pass


