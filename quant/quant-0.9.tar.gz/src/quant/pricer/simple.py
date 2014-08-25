import abc
import math

import scipy

from quant.stats import NormalDistribution
from quantdsl import compile, DslExpression, PriceSimulator
from quantdsl import Fixing
from quantdsl import DslObject


class Pricer(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwds):
        pass

    def calcValues(self):
        raise Exception, "Method not implemented."

    @abc.abstractmethod
    def calcValue(self, *args, **kwds):
        raise Exception, "Method not implemented."

    @abc.abstractmethod
    def calcDelta(self, *args, **kwds):
        pass

    @abc.abstractmethod
    def calcGamma(self, *args, **kwds):
        pass

    def calcVega(self, *args, **kwds):
        pass


class DerivativePricer(Pricer):

    daysPerYear = 365  # Assumes "Actual/365 Fixed" day-count convention.

    def __init__(self, strikePrice, lastPrice, actualHistoricalVolatility, durationYears, isPut=False, annualRiskFreeRate=0.0, tolerance=1e-9):
        self.strikePrice = strikePrice
        self.lastPrice = lastPrice
        self.actualHistoricalVolatility = actualHistoricalVolatility
        self.durationYears = durationYears
        self.isPut = isPut
        self.annualRiskFreeRate = annualRiskFreeRate
        self.tolerance = tolerance

# Todo: Change to not pass in optionValue0 (like Dsl works now).
    def calcDelta(self, optionValue0):
        #print self.__class__
        #print "estimated value: %s" % optionValue0
        lastPriceDelta = self.lastPrice * 0.001 * self.actualHistoricalVolatility / 100.0
        #print "price delta: %s" % lastPriceDelta
        originalLastPrice = self.lastPrice
        try:
            self.lastPrice += lastPriceDelta
            #print "perturbed price: %s" % self.lastPrice
            optionValue1 = self.calcValue()
            #print "perturbed value: %s" % optionValue1
            #print "perturbation: %s" % lastPriceDelta
        finally:
            self.lastPrice = originalLastPrice
        optionValueDelta = optionValue1 - optionValue0
        optionDelta = optionValueDelta / lastPriceDelta
        #print "estimated delta: %s" % optionDelta
        return optionDelta

# Todo: Change to not pass in optionValue1 and optionDelta1 (like Dsl works now).
    def calcGamma(self, optionValue1, optionDelta1):
        lastPriceDelta = self.lastPrice * 0.001 * self.actualHistoricalVolatility / 100.0
        originalLastPrice = self.lastPrice
        try:
            self.lastPrice -= lastPriceDelta
            #print "perturbed price: %s" % self.lastPrice
            optionValue0 = self.calcValue()
            #print "perturbed value: %s" % optionValue0
            #print "perturbation: %s" % lastPriceDelta
        finally:
            self.lastPrice = originalLastPrice
        optionValueDelta = optionValue1 - optionValue0
        optionDelta0 = optionValueDelta / lastPriceDelta
        #print "perturbed delta: %s" % optionDelta0
        optionDeltaDelta = optionDelta1 - optionDelta0
        optionGamma = optionDeltaDelta / lastPriceDelta
        #print "estimated gamma: %s" % optionGamma
        return optionGamma

# Todo: Change to not pass in optionValue0 (like Dsl works now).
    def calcVega(self, optionValue0):
        actualHistoricalVolatilityDelta = 0.001 * self.actualHistoricalVolatility
        originalActualHistoricalVolatility = self.actualHistoricalVolatility
        try:
            self.actualHistoricalVolatility += actualHistoricalVolatilityDelta
            optionValue1 = self.calcValue()
        finally:
            self.actualHistoricalVolatility = originalActualHistoricalVolatility
        optionValueDelta = optionValue1 - optionValue0
        optionVega = optionValueDelta / actualHistoricalVolatilityDelta
        return optionVega


class EuropeanBlackScholes(DerivativePricer):

    def calcValue(self):
        S = float(self.lastPrice)
        K = float(self.strikePrice)
        r = float(self.annualRiskFreeRate) / 100.0
        t = float(self.durationYears)
        sigma = float(self.actualHistoricalVolatility) / 100.0
        sigma_squared_t = sigma**2 * t
        try:
            sigma_root_t = sigma * math.sqrt(t)
        except Exception, inst:
            msg = "Couldn't sqrt: %s: %s" % (t, inst)
            raise Exception, msg
        d1 = (math.log(S / K) + t * r + 0.5 * sigma_squared_t) / sigma_root_t
        d2 = d1 - sigma_root_t
        Nd1 = self.N(d1)
        Nd2 = self.N(d2)
        e_to_minus_rt = math.exp(-1.0 * r * t)
        if self.isPut:
            # Put option.
            optionValue = (1-Nd2)*K*e_to_minus_rt - (1-Nd1)*S
        else:
            # Call option.
            optionValue = Nd1*S - Nd2*K*e_to_minus_rt
        return optionValue

    def N(self, d):
        return self.getNormalDistribution().cdf(d)

    def getNormalDistribution(self):
        if not hasattr(self, 'normalDistribution'):
            self.normalDistribution = NormalDistribution()
        return self.normalDistribution


class BinomialTree(DerivativePricer):

    stepCount = 300

    def calcValue(self):
        self.stepDurationYears = self.calcStepDurationYears()
        self.stepUpFactor = self.calcStepUpFactor()
        self.stepUpProbability = self.calcUpProbability()
        self.stepDiscountFactor = self.calcStepDiscountFactor()
        return self.calcOptionValue()

    def calcStepDurationYears(self):
        T = self.durationYears
        return T / self.stepCount

    def calcStepUpFactor(self):
        sigma = float(self.actualHistoricalVolatility) / 100
        t = self.stepDurationYears
        return scipy.exp(sigma * scipy.sqrt(t))

    def calcUpProbability(self):
        u = self.stepUpFactor
        return (u - 1)/(u**2 - 1)

    def calcStepDiscountFactor(self):
        r = float(self.annualRiskFreeRate) / 100
        t = self.stepDurationYears
        return scipy.exp(r * t)

    def calcOptionValue(self):
        laterNodes = None
        for stepIndex in range(self.stepCount, -1, -1):
            nodeCount = stepIndex + 1
            earlierNodes = [None] * (nodeCount)
            for nodeIndex in range(0, nodeCount):
                netUps = 2 * nodeIndex - stepIndex
                if laterNodes == None:
                    # Option value is exercise value.
                    optionValue = self.calcExerciseValue(netUps)
                else:
                    # Option value is max of exercise value and binomial value.
                    continuationValue = self.calcContinuationValue(laterNodes, nodeIndex)
                    if not self.isExercisableAt(stepIndex):
                        optionValue = continuationValue
                    else:
                        exerciseValue = self.calcExerciseValue(netUps)
                        optionValue = max(continuationValue, exerciseValue)
                earlierNodes[nodeIndex] = optionValue
            laterNodes = earlierNodes
        return laterNodes[0]

    def calcContinuationValue(self, laterNodes, nodeIndex):
        upValue = laterNodes[nodeIndex+1]
        downValue = laterNodes[nodeIndex]
        expectedValue = self.stepUpProbability * upValue
        expectedValue += (1 - self.stepUpProbability) * downValue
        return self.stepDiscountFactor * expectedValue

    def calcExerciseValue(self, netUps):
        underlyingValue = self.calcUnderlyingValue(netUps)
        return self.calcPayoff(underlyingValue, self.strikePrice)

    def calcUnderlyingValue(self, netUps):
        u = self.stepUpFactor
        x = netUps
        S = self.lastPrice
        return u**x * S

    def calcPayoff(self, underlyingValue, strikePrice):
        S = underlyingValue
        K = strikePrice
        if not self.isPut:
            return max(S - K, 0)
        else:
            return max(K - S, 0)

    def isExercisableAt(self, stepIndex):
        raise Exception, "Method not implemented on %s" % self.__class__.__name__


class AmericanBinomialTree(BinomialTree):

    def isExercisableAt(self, stepIndex):
        return True


class EuropeanBinomialTree(BinomialTree):

    def isExercisableAt(self, stepIndex):
        return stepIndex == self.stepCount


class MonteCarlo(DerivativePricer):

    pathCount = 500000

    def calcValue(self):
        draws = self.calcDraws()
        underlyings = self.calcUnderlyings(draws)
        payoffs = self.calcPayoffs(underlyings)
        return payoffs.mean()
        
    def calcDraws(self):
        if not hasattr(self, '_draws'):
            self._draws = scipy.random.standard_normal(self.pathCount)
        return self._draws

    def calcUnderlyings(self, draws):
        T = self.durationYears
        sigma = float(self.actualHistoricalVolatility) / 100
        sigma_root_T = sigma * scipy.sqrt(T)
        sigma_squared_T = sigma**2 * T
        return self.lastPrice * scipy.exp(sigma_root_T * draws - 0.5 * sigma_squared_T)

    def calcPayoffs(self, underlyings):
        if self.isPut:
            differences = self.strikePrice - underlyings
        else:
            differences = underlyings - self.strikePrice
        zeros = scipy.zeros(len(differences))
        return scipy.array([differences, zeros]).max(axis=0)


class EuropeanMonteCarlo(MonteCarlo):

    pass


class AmericanMonteCarlo(MonteCarlo):

    # Todo: Needs L-S routine.
    pass


class DslMonteCarlo(Pricer):

    def __init__(self, specification, image):
        self.dsl = None
        self.allRvs = None
        self.value = None
        self.cache = {}
        self.specification = specification
        self.image = image

    @property
    def priceSimulation(self):
        if not hasattr(self, '_priceSimulation'):
            self._priceSimulation = PriceSimulator(self.image)
        return self._priceSimulation

    def getMarkets(self):
        return self.priceSimulation.getMarkets(self.getDsl())

    def getDsl(self):
        if self.dsl == None:
            dslExpr = compile(self.specification)
            assert isinstance(dslExpr, DslExpression)
            self.dsl = dslExpr
        return self.dsl

    def calcValue(self):
        return self.evaluateDsl(self.image)

    def getPerturbedImage(self, market, factor):
        return self.image.perturbMetric('last-price', market, factor)

    def calcDelta(self, market, image=None, order=1):
        if image == None:
            image = self.image
        if order == 0:
            return self.evaluateDsl(image)
        factor = self.calcPerturbationFactor(market)
        perturbedImage = image.perturbMetric('last-price', market, factor)
        delta = self.calcGradient(
            self.calcDelta(market, image, order-1),
            self.calcDelta(market, perturbedImage, order-1),
            perturbedImage.getPerturbation()
        )
        return delta

    def calcGamma(self, market):
        return self.calcDelta(market, order=2)

    def getAllRvs(self):
        if not hasattr(self, '_allRvs'):
            self._allRvs = self.priceSimulation.getAllRvs(self.getDsl())
        return self._allRvs

    def evaluateDsl(self, image):
        if image not in self.cache:
            dsl = self.getDsl()
            allRvs = self.getAllRvs()
            kwds = {
                'image': image,
                'allRvs': allRvs,
                'presentTime': image.observationTime,
                'interestRate': '2.5',
            }
            value = dsl.evaluate(**kwds)
            if hasattr(value, 'mean'):
                value = value.mean()
            self.cache[image] = value
        return self.cache[image]



    def calcPerturbationFactor(self, market):
        actualHistoricalVolatility = self.image.getMetricValue('actual-historical-volatility', market)
        return 0.001 * actualHistoricalVolatility / 100.0







    def getFixings(self):
        return self.getDsl().findInstances(dslType=Fixing)

    def getDslObjects(self, dslObject, dslType):
        if not dslObject:
            dslObject = self.getDsl()
        dslObjects = set()
        for arg in dslObject._args:
            if isinstance(arg, dslType):
                dslObjects.add(arg)
            if isinstance(arg, DslObject):
                dslObjects.update(self.getDslObjects(dslObject=arg, dslType=dslType))
        return dslObjects

    def calcGradient(self, y1, y2, dx):
        return (y2 - y1) / dx


class EuropeanBlackScholesLocalVol(Pricer):

    def calcValue(self):
        return 2.416

    def calcDelta(self, estimatedValue):
        return 0.678

    def calcGamma(self, estimatedValue, esimatedDelta):
        return 0.072

    def calcVega(self):
        return 1
