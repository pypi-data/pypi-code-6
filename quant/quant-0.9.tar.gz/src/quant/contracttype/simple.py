from dm.dom.stateful import *

class PricerNotDefined(Exception): pass

class Contract(DatedStatefulObject):

    title = String()
    book = HasA("Book", isRequired=False)

    def getLabelValue(self):
        return self.title or self.id

    def getContractType(self):
        codeClassName = self.meta.name
        return self.registry.contractTypes.read(codeClassName=codeClassName)

    def calcResults(self, result):
        raise Exception, "Method 'calcResults' not implemented on %s." % self.__class__ 

    def getPricer(self, priceProcess):
        if not hasattr(self, '_pricer'):
            contractType = self.getContractType()
            preference = contractType.pricerPreferences.get(priceProcess, None)
            if preference:
                self._pricer = preference.pricer
            else:
                msg = "No pricer preference exists for evaluating "
                msg += "'%s' contracts with " % self.__class__.__name__
                msg += "the '%s' price process." % priceProcess.codeClassName
                raise PricerNotDefined, msg
        return self._pricer

    def saveResult(self, result, metricName, metricValue, market, pricer=None):
        result.addLine(
            contract=self,
            metricName=metricName,
            metricValue=metricValue,
            market=market,
            pricer=pricer,
        )


class Derivative(Contract):

    underlying = HasA('Market', isRequired=True)
    volume = Float(isRequired=True)


class Option(Derivative):

    settlement = Date(isRequired=True)
    strikePrice = Float()
    expiration = Date()
    right = HasA('OptionRight', isSimpleOption=True)

    def calcResults(self, result):
        pricer = self.getPricer(result.image.priceProcess)
        lastPrice = result.image.getMetricValue(
            'last-price', self.underlying
        )
        actualHistoricalVolatility = result.image.getMetricValue(
            'actual-historical-volatility', self.underlying
        )
        nowTime = result.image.observationTime
        expiration = self.expiration
        durationYears = result.image.priceProcess.getDurationYears(nowTime, expiration)
        pricerCode = pricer.getCodeClass()(
            isPut=bool(self.right.name == 'Put'),
            strikePrice=self.strikePrice,
            lastPrice=lastPrice,
            actualHistoricalVolatility=actualHistoricalVolatility,
            durationYears=durationYears
        )
        unitValue = pricerCode.calcValue()
        unitDelta = pricerCode.calcDelta(unitValue)
        unitGamma = pricerCode.calcGamma(unitValue, unitDelta)
        unitVega = pricerCode.calcVega(unitValue)
        contractValue = self.volume * unitValue
        contractDelta = self.volume * unitDelta
        contractGamma = self.volume * unitGamma
        contractVega = self.volume * unitVega
        self.saveResult(result, result.PRESENT_VALUE_METRIC, contractValue, pricer)
        self.saveResult(result, result.DELTA_METRIC, contractDelta, pricer)
        self.saveResult(result, result.GAMMA_METRIC, contractGamma, pricer)
        self.saveResult(result, result.VEGA_METRIC, contractVega, pricer)

    def saveResult(self, result, metricName, metricValue, pricer=None):
        super(Derivative, self).saveResult(
            result=result,
            metricName=metricName,
            metricValue=metricValue,
            market=self.underlying,
            pricer=pricer,
        )


class OptionRight(NamedObject):

    pass


class American(Option):

    pass


class Binary(Option):

    pass


class Dsl(Contract):
    
    specification = Text(isRequired=True)

    def calcResults(self, result):
        pricer = self.getPricer(result.image.priceProcess)
        specification = self.specification.replace('\r\n', '\n')
        originalImage = result.image
        pricerCode = pricer.getCodeClass()(
            specification=specification,
            image=originalImage,
        )
        estimatedValue = pricerCode.calcValue()
        self.saveResult(
            result=result,
            metricName=result.PRESENT_VALUE_METRIC,
            metricValue=estimatedValue,
            market=None,
            pricer=pricer,
        )
        for market in pricerCode.getMarkets():
            estimatedDelta = pricerCode.calcDelta(market)
            self.saveResult(
                result=result,
                metricName=result.DELTA_METRIC,
                metricValue=estimatedDelta,
                market=market,
                pricer=pricer,
            )
            estimatedGamma = pricerCode.calcGamma(market)
            self.saveResult(
                result=result,
                metricName=result.GAMMA_METRIC,
                metricValue=estimatedGamma,
                market=market,
                pricer=pricer,
            )


class European(Option):

    pass


class Futures(Derivative):

    registryAttrName = 'futures'

    futuresPrice = Float(isRequired=True)
    right = HasA('FuturesRight', isRequired=True, isSimpleOption=True)

    def calcResults(self, result):
        lastPrice = result.image.getMetricValue('last-price', self.underlying)
        contractValue = (lastPrice - self.futuresPrice) * self.volume
        contractDelta = self.volume
        contractGamma = 0
        if self.right.name == 'Buy':
            contractValue *= -1
            contractDelta *= -1
            contractGamma *= -1
        self.saveResult(result, result.PRESENT_VALUE_METRIC, contractValue)
        self.saveResult(result, result.DELTA_METRIC, contractDelta)
        self.saveResult(result, result.GAMMA_METRIC, contractGamma)

    def saveResult(self, result, metricName, metricValue):
        super(Futures, self).saveResult(
            result=result,
            metricName=metricName,
            metricValue=metricValue,
            market=self.underlying,
        )


class FuturesRight(NamedObject):

    pass



class Swap(Derivative):

    # Todo: More about swaps.
    pass


