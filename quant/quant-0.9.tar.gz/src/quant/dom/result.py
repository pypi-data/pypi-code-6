from quant.dom.base import SimpleObject
from quant.dom.base import DatedObject
from quant.dom.base import String
from quant.dom.base import AggregatesMany
from quant.dom.base import HasA
from quant.dom.base import Integer
from quant.dom.base import Float
from quant.dom.base import Boolean
import datetime
import dateutil.parser

# Todo: Make image metrics and result lines more similar? 

class Result(DatedObject):

    PRESENT_VALUE_METRIC = 'value'
    DELTA_METRIC = 'delta'
    GAMMA_METRIC = 'gamma'
    VEGA_METRIC = 'vega'

    isUnique = False
    sortOnName = 'id'
    sortAscending = False

    book = HasA('Book')
    image = HasA('Image')
    doCalculationsLater = Boolean(isHidden=True)
    lines = AggregatesMany('ResultLine', key='id', isEditable=False)
    totalValue = Float(isEditable=False)

    def getLabelValue(self):
        return '#%s: %s with Image %s' % (self.id, self.book.getLabelValue(), self.image.getLabelValue())

    def onCreate(self):
        super(Result, self).onCreate()
        if not self.doCalculationsLater:
            self.calcResults()

    def calcResults(self):
        if len(self.lines):
            raise Exception, "Results already calculated for Result #%s." % self.id
        for contract in self.book.getContracts():
            contract.calcResults(result=self)
        self.totalValue = self.getTotalValue()
        self.save()

    def addLine(self, contract, metricName, metricValue, market, pricer):
        self.lines.create(
           contractId=contract.id,
           contractType=contract.meta.name,
           contractRegisterName=contract.getRegistryAttrName(),
           contractLabel=contract.getLabelValue(),
           metricName=metricName,
           metricValue=float(metricValue),
           market=market,
           pricer=pricer,
        )

    def getTotalValue(self):
        totalValue = 0
        for line in self.lines:
            if line.metricName == self.PRESENT_VALUE_METRIC:
                totalValue += line.metricValue
        return totalValue

    def getGreeksByMarket(self):
        markets = []
        marketDeltas = {}
        marketGammas = {}
        marketVegas = {}
        greeks = [self.DELTA_METRIC, self.GAMMA_METRIC, self.VEGA_METRIC]
        for line in self.lines:
            if not line.market:
                continue
            market = line.market
            if market not in markets:
                markets.append(market)
                marketDeltas[market.id] = 0.0
                marketGammas[market.id] = 0.0
                marketVegas[market.id] = 0.0
            metricName = line.metricName
            metricValue = line.metricValue
            if metricName == self.DELTA_METRIC:
                marketDeltas[market.id] += metricValue
            elif metricName == self.GAMMA_METRIC:
                marketGammas[market.id] += metricValue
            elif metricName == self.VEGA_METRIC:
                marketVegas[market.id] += metricValue
        greeksByPeriod = [{'market': p, 'delta': marketDeltas[p.id], 'gamma': marketGammas[p.id], 'vega': marketVegas[p.id]} for p in markets]
        return greeksByPeriod

    def getValuesByContract(self):
        contracts = []
        contractValues = {}
        valueLines = []
        for line in self.lines:
            if line.metricName == self.PRESENT_VALUE_METRIC:
                valueLines.append(line)
        for line in valueLines:
            contract = self.getContract(line.contractType, line.contractId)
            if contract not in contracts:
                contracts.append(contract)
                contractValues[contract] = 0
            contractValues[contract] += line.metricValue
        return [{'contract': c, 'contractValue': contractValues[c]} for c in contracts]

    def getContract(self, contractType, contractId):
        contractClass = self.registry.getDomainClass(contractType)
        contractRegister = contractClass.createRegister()
        return contractRegister[contractId]

    def getPricer(self, pricerLabel):
        codeClassName = pricerLabel.split('.')[-1]
        codeModuleName = '.'.join(pricerLabel.split('.')[:-1])
        return self.registry.pricers.findSingleDomainObject(codeModuleName=codeModuleName, codeClassName=codeClassName)


class ResultLine(SimpleObject):

    isUnique = False
    sortOnName = 'id'

    result = HasA('Result')
    contractId = Integer()
    contractType = String()
    contractRegisterName = String()
    contractLabel = String()
    market = HasA('Market')
    pricer = HasA('Pricer', isRequired=False)
    metricName = String()
    metricValue = Float()

    def getContract(self):
        if not hasattr(self, '_contract'):
            self._contract = self.result.getContract(self.contractType, self.contractId)
        return self._contract

    def getPricer(self):
        return self.pricer

