import sys
from quant.dom.base import StandardObject
from quant.dom.base import SimpleObject
from quant.dom.base import NamedObject
from quant.dom.base import DatedStatefulObject
from quant.dom.base import String
from quant.dom.base import Text 
from quant.dom.base import Date
from quant.dom.base import AggregatesMany
from quant.dom.base import HasMany
from quant.dom.base import HasA
from quant.dom.base import Float
from quant.dom.base import DateTime
from quant.dom.base import Boolean
import datetime
import dateutil.parser
import scipy
import math

class Exchange(NamedObject):

    symbols = AggregatesMany('Symbol', key='name', ownerName='exchange')
    holidays = Text(isRequired=False)


class Symbol(NamedObject):

    markets = AggregatesMany('Market', key='id')
    exchange = HasA('Exchange', isRequired=True, isSimpleOption=True)


class Value(SimpleObject):

    sortOnName = 'observationTime'
    sortAscending = False

    value = Float(isRequired=True)
    observationTime = DateTime(isRequired=True)
    market = HasA('Market', isRequired=True)


# Todo: Rename to FuturesMarket.
class Market(SimpleObject):
   

    monthLetters = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']

    isTemporal = True

    firstDeliveryDate = Date()
    expiration = Date()
    sortOnName = 'firstDeliveryDate'
    symbol = HasA('Symbol', isRequired=True)
    history = HasMany('Value', key='id')
    metrics = AggregatesMany('Metric', key='id', isEditable=False)
    europeanOptionMarkets = AggregatesMany('EuropeanOptionMarket', key='id')


    def getLabelValue(self):
        monthIndex = self.firstDeliveryDate.month - 1
        monthLetter = self.monthLetters[monthIndex]
        yearAbbr = str(self.firstDeliveryDate.year)[2:]
        return self.symbol.getLabelValue() + '.' + monthLetter + yearAbbr

    def calcLastPrice(self, observationTime):
        # Todo: Look up effective value at observation time.
        history = list(self.history)
        if len(history):
            return history[0].value
        else:
            raise Exception, "Price history has zero length."

    def getPriceHistory(self, observationTime):
        # Todo: Return history only until observation time.
        return list(self.history)


class EuropeanOptionMarket(SimpleObject):

    market = HasA('Market', isRequired=True)
    strikePrice = Float(isRequired=True)
    expiration = Date()

    def getLabelValue(self):
        return self.market.getLabelValue() + '.' + self.expiration.strftime('%c') + '.' + str(self.strikePrice)
        monthIndex = self.firstDeliveryDate.month - 1
        monthLetter = self.monthLetters[monthIndex]
        yearAbbr = str(self.firstDeliveryDate.year)[2:]
        return '%s.%s.%s' % (self.market.getLabelValue(), self.expiration.strftime('%c'), self.strikePrice)



class Image(SimpleObject):

    isUnique = False
    sortOnName = 'id'
    sortAscending = False
    observationTime = DateTime()
    priceProcess = HasA('PriceProcess', isRequired=True)
    results = AggregatesMany('Result', key='id')
    metrics = AggregatesMany('Metric', key='id')

    def getLabelValue(self):
        return "#%s: %s at %s" % (self.id, self.priceProcess.codeClassName, self.meta.attributeNames['observationTime'].createLabelRepr(self))

    def getMetricValue(self, metricName, market):
        metrics = self.metrics.findDomainObjects(metricName=metricName, market=market)
        if len(metrics) > 1:
            raise Exception, "There are %s values for metric '%s' and market '%s'." % (len(metrics), metricName, market)
        elif len(metrics) == 1:
            metricValue = metrics[0].metricValue
        else:
            metricValue = self.priceProcess.getMetricValue(metricName=metricName, market=market, observationTime=self.observationTime)
            self.metrics.create(metricValue=metricValue, metricName=metricName, market=market)
        return metricValue

    def perturbMetric(self, metricName, market, factor):
        return PerturbedImage(self, metricName, market, factor)


class PerturbedImage(object):

    def __init__(self, originalImage, metricName, market, factor):
        self.originalImage = originalImage
        self.metricName = metricName
        self.market = market
        self.factor = factor

    def __getattribute__(self, item):
        if item in ['getMetricValue', 'getPerturbation', 'originalImage', 'metricName', 'market', 'factor']:
            return object.__getattribute__(self, item)
        return getattr(self.originalImage, item)

    def getMetricValue(self, metricName, market):
        value = self.originalImage.getMetricValue(metricName, market)
        if metricName == self.metricName and market == self.market:
            value += self.factor * value
        return value

    def getPerturbation(self):
        return self.factor * self.originalImage.getMetricValue(self.metricName, self.market)


class Metric(SimpleObject):

    isUnique = False
    sortOnName = 'id'

    image = HasA('Image')
    market = HasA('Market')
    metricName = String()
    metricValue = Float()

