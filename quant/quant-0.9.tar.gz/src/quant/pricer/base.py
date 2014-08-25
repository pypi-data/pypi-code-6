from scipy.stats import norm
from scipy import integrate
from scipy import exp, log, sqrt, pi
from math import sqrt
from quant.exceptions import PricerLimitError
import dateutil.parser
from quant.stats import NormalDistribution
from quant.stats import LogNormalDistribution


# Todo: Define holidays on symbol.
# Todo: Introduce Exchange object and define holidays for exchange.
# Todo: Support variations in holidays for different 
# Todo: Model different trading modes (open call, electronic, etc.).
# Todo: Figure out whether price "moves" on holidays (event can happen).

#import workdays
#
#class Holidays(list): pass
#
#    Date U.S. Holiday
#    23-26 December 2010 (PDF)   Christmas
#    31 December 2010 - 3 January 2011 (PDF) New Year's
#    14-18 January 2011 (PDF)    Dr. Martin Luther King, Jr.
#    18-22 February 2011 (PDF)   President's Day
#    21-24 April 2011 (PDF)  Good Friday
#    27-31 May 2011 (PDF)    Memorial Day
#    1-5 July 2011 (PDF) Independence Day
#    2-6 September 2011 (PDF)    Labor Day
#    7-10 October 2011 (PDF) Columbus Day
#    10-11 November 2011 (PDF)   Veteran's Day
#    23-25 November 2011 (PDF)   Thanksgiving
#    23-27 December 2011 (PDF)   Christmas
#    30 December 2011 - 3 January 2012 (PDF) New Year's
#
#
#class Workdays(object):
#
#    def countWorkdays(start, end):
#        return workdays.networkdays(start, end, Holidays())
#
#
#class AbstractIntegralLimits(object):
#
#    def getIntegralUpperLimit(self):
#        raise Exception, "Method not implemented."
#
#    def getIntegralLowerLimit(self):
#        raise Exception, "Method not implemented."
#
#
#class CallIntegralLimits(AbstractIntegralLimits):
#
#    def getIntegralLowerLimit(self):
#        highPercentile = self.lastPrice + self.INTEGRAL_WIDTH * self.actualHistoricalVolatility
#        lowPercentile = self.lastPrice - self.INTEGRAL_WIDTH * self.actualHistoricalVolatility
#        if self.strikePrice < lowPercentile:
#            lowerLimit = lowPercentile
#        elif self.strikePrice > highPercentile:
#            lowerLimit = highPercentile
#        else:
#            lowerLimit = self.strikePrice
#        return lowerLimit
#
#    def getIntegralUpperLimit(self):
#        highPercentile = self.lastPrice + self.INTEGRAL_WIDTH * self.actualHistoricalVolatility
#        upperLimit = highPercentile
#        return upperLimit
#
#
#class PutIntegralLimits(AbstractIntegralLimits):
#
#    def getIntegralLowerLimit(self):
#        lowPercentile = self.lastPrice - self.INTEGRAL_WIDTH * self.actualHistoricalVolatility
#        lowerLimit = lowPercentile
#        # Todo: Use a log-normal distribution rather than normal distribution to avoid negative integral limit errors.
#        if lowerLimit < 0:
#            msg = "Given current price (%f) the actualHistoricalVolatility (%f) is too high to value European Put Option with price movements based on the normal distribution." % (self.lastPrice, self.actualHistoricalVolatility)
#            raise PricerLimitError, msg
#        return lowerLimit
#
#    def getIntegralUpperLimit(self):
#        highPercentile = self.lastPrice + self.INTEGRAL_WIDTH * self.actualHistoricalVolatility
#        lowPercentile = self.lastPrice - self.INTEGRAL_WIDTH * self.actualHistoricalVolatility
#        if self.strikePrice < lowPercentile:
#            upperLimit = lowPercentile
#        elif self.strikePrice > highPercentile:
#            upperLimit = highPercentile
#        else:
#            upperLimit = self.strikePrice
#        return upperLimit
#
#
#class WienerPricer(AbstractOptionPricer, AbstractIntegralLimits):
#
#    VOLATILITY_LIMIT_INFINITESIMAL = 0.000000001
#    INTEGRAL_WIDTH = 7
#
#    def setActualHistoricalVolatility(self, actualHistoricalVolatility):
#        value = actualHistoricalVolatility
#        limit = self.VOLATILITY_LIMIT_INFINITESIMAL
#        self.actualHistoricalVolatility = abs(value) > limit and value or limit
#
#    def calcPrice(self):
#        raise Exception, "Balh"
#        integralLowerLimit = self.getIntegralLowerLimit()
#        integralUpperLimit = self.getIntegralUpperLimit()
#        self.optionDurationVolatility = self.getOptionDurationVolatility()
#        if integralLowerLimit < 0:
#            raise PricerLimitError, "Integral lower limit is negative: %s" % integralLowerLimit
#        if integralUpperLimit < 0:
#            raise PricerLimitError, "Integral upper limit is negative: %s" % integralUpperLimit
#        integral = integrate.quadrature(
#            func=self.payoffDensity,
#            a=integralLowerLimit,
#            b=integralUpperLimit,
#            tol=self.tolerance,
#            maxiter=500
#        )
#        estimate = integral[0]
#        absError = integral[1]
#        if absError > self.tolerance:
#            msg = "Absolute error out of tolerance: %f" % absError
#            raise Exception, msg
#        return estimate
#
#    def payoffDensity(self, x):
#        raise Exception, "Method not implemented."
#
#    def getGaussianDensity(self, x):
#        from scipy.stats import norm
#        return self.normPdf(x)
#
#    def getProbabilityDensity(self, x):
#        pdf = self.getProbabilityDensityFunction()
#        return pdf(x)
#
#    def getProbabilityDensityFunction(self):
#        if not hasattr(self, 'probabilityDensityFunction'):
#            self.probabilityDensityFunction = self.createProbabilityDensityFunction()
#        return self.probabilityDensityFunction
#    
#    def createProbabilityDensityFunction(self):
#        distribution = LogNormalDistribution(
#            mean=self.lastPrice, 
#            variance=self.optionDurationVolatility**2,
#        )
#        return distribution.pdf
#
#    def normPdf(self, x):
#        return norm.pdf(x, loc=self.lastPrice, scale=self.optionDurationVolatility)
#
#    def getOptionDurationVolatility(self):
#        optionDurationDays = self.getOptionDuration().days
#        annualDurationDays = 365.0
#        optionDurationYears = self.getOptionDurationYears()
#        optionDurationVolatility = self.scaleVolatility(optionDurationYears)
#        return optionDurationVolatility
#
#
