import unittest
from quant.testunit import TestCase

from quant.stats import NormalDistribution
from quant.stats import LogNormalDistribution
from scipy import exp, log, sqrt, pi

def suite():
    suites = [
        unittest.makeSuite(TestNormalDistribution),
        unittest.makeSuite(TestNormalDistributionNonStandard),
        unittest.makeSuite(TestLogNormalDistribution),
        unittest.makeSuite(TestLogNormalDistributionNonStandard),
    ]
    return unittest.TestSuite(suites)


class RandomVariableTestCase(TestCase):
 
    DECIMALS = 14

    def setUp(self):
        self.crv = self.create()

    def testPdf(self):
        self.assertEqual(self.getPdf(1e-7), self.calcPdf(1e-7))
        self.assertEqual(self.getPdf(1e-3), self.calcPdf(1e-3))
        self.assertEqual(self.getPdf(1), self.calcPdf(1))
        self.assertEqual(self.getPdf(2), self.calcPdf(2))
        self.assertEqual(self.getPdf(3), self.calcPdf(3))
        self.assertEqual(self.getPdf(4), self.calcPdf(4))
        self.assertEqual(self.getPdf(5), self.calcPdf(5))
        self.assertEqual(self.getPdf(10), self.calcPdf(10))
        self.assertEqual(self.getPdf(100), self.calcPdf(100))

    def testCdf(self):
        self.assertEqual(self.getCdf(1e-7), self.calcCdf(1e-7))
        self.assertEqual(self.getCdf(1e-3), self.calcCdf(1e-3))
        self.assertEqual(self.getCdf(1), self.calcCdf(1))
        self.assertEqual(self.getCdf(2), self.calcCdf(2))
        self.assertEqual(self.getCdf(3), self.calcCdf(3))
        self.assertEqual(self.getCdf(4), self.calcCdf(4))
        self.assertEqual(self.getCdf(5), self.calcCdf(5))
        self.assertEqual(self.getCdf(10), self.calcCdf(10))
        self.assertEqual(self.getCdf(100), self.calcCdf(100))

    def testDraw(self):
        self.getDraw()

    def assertEqual(self, a, b):
        a = round(a, self.DECIMALS)
        b = round(b, self.DECIMALS)
        super(RandomVariableTestCase, self).assertEqual(a, b)

    def getPdf(self, x):
        return self.crv.pdf(x)

    def getCdf(self, x):
        return self.crv.cdf(x)

    def getDraw(self):
        return self.crv.draw()

    def create(self, x):
        raise Exception, "Method not implemented."

    def calcPdf(self, x):
        raise Exception, "Method not implemented."

    def calcCdf(self, x):
        raise Exception, "Method not implemented."


class NormalDistributionTestCase(RandomVariableTestCase):

    mean = 0
    variance = 1

    def create(self):
        return NormalDistribution(mean=self.mean, variance=self.variance)

    def calcPdf(self, x):
        return (exp(-1.0 * ((x - self.mean) ** 2.0) / (2.0 * self.variance))) / sqrt(2.0 * pi * self.variance)

    def calcCdf(self, x):
        if x == 0:
            return 0.5
        elif x == 1e-7:
            return 0.50000003989423003
        elif x == 1e-3:
            return 0.50039894221391001
        elif x == 1:
            return 0.84134474606854004
        elif x == 2:
            return 0.97724986805182001
        elif x == 3:
            return 0.99865010196837001
        elif x == 4:
            return 0.99996832875816999
        elif x == 5:
            return 0.99999971334842996
        elif x == 10:
            return 1.0  
        elif x == 100:
            return 1.0
        else:
            raise Exception, "Can't calc CDF for: %s" % x

class TestNormalDistribution(NormalDistributionTestCase): pass

class TestNormalDistributionNonStandard(NormalDistributionTestCase):
    mean = 2
    variance = 3

    def testCdf(self):
        pass

class LogNormalDistributionTestCase(NormalDistributionTestCase):

    def create(self):
        return LogNormalDistribution(
            mean=self.mean,
            variance=self.variance
        )

    def calcPdf(self, x):
        return (exp(-1.0 * ((log(x) - self.mean)**2) / (2 * self.variance) )) / (x * sqrt(self.variance) * sqrt(2 * pi))

    def testCdf(self):
        pass

class TestLogNormalDistribution(LogNormalDistributionTestCase): pass

class TestLogNormalDistributionNonStandard(LogNormalDistributionTestCase):

    mean = 2
    variance = 3


