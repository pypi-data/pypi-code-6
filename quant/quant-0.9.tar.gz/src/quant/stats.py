from scipy.stats import norm
from scipy.stats import lognorm
from scipy import exp, log, sqrt, pi

class RandomVariable(object):

    def getRv(self):
        if not hasattr(self, '_rv'):
            self._rv = self.createRv()
        return self._rv

    rv = property(getRv)

    def createRv(self):
        raise Exception, "Method not implemented."


class ContinuousRandomVariable(RandomVariable):

    def pdf(self, x):
        raise Exception, "Method not implemented."

    def cdf(self, x):
        raise Exception, "Method not implemented."

    def draw(self):
        raise Exception, "Method not implemented."


class NormalDistribution(ContinuousRandomVariable):

    def __init__(self, mean=0, variance=1):
        self.mean = mean
        self.variance = variance

    def createRv(self):
        loc = self.mean
        scale = sqrt(self.variance)
        return norm(loc=loc, scale=scale)

    def pdf(self, x):
        return self.rv.pdf(x)

    def cdf(self, x):
        return self.rv.cdf(x)

    def draw(self):
        return self.rv.rvs()


class LogNormalDistribution(NormalDistribution):

    def createRv(self):
        shape = sqrt(self.variance)
        scale = exp(self.mean)
        return lognorm(shape, scale=scale)

