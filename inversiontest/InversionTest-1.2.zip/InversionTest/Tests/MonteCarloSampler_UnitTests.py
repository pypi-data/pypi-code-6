import unittest
import math
from random import Random, uniform, randint, choice, gauss, shuffle
from InversionTest.Constants import (GREATER_THAN_HYPOTHESIS,
    LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS)
from InversionTest.MonteCarloSampler import (MCBMeanDifferenceTest,
    MCBStoppingRuleTest, MCBWilcoxonRankTest, MCHypothesisTest,
    MCMeanDifferenceTest, MCWilcoxonRankTest, MonteCarloEstimator,
    convertSamplesToRanks, meanDifference, wilcoxonRankSum,)

# NOTE: Since Monte Carlo is a random process, random seed is fixed to a value
#       where all tests should run successfully.  If tests fail, it is because
#       something has been broken.

def cauchy(location, scale):
    """ Cauchy distribution """
    x = random()
    while x == 0.0:
        x = random()
    return location + scale*math.tan(math.pi*(x - 0.5))

RANDOM_GEN = Random(100).random

def staticShuffle(x, rGen=RANDOM_GEN):
    shuffle(x, rGen)
    return x

def forceStaticSampling(cls):
    def _sampleFunction(self):
        staticShuffle(self._combinedSample)
        return self._combinedSample
    cls._sampleFunction = _sampleFunction
    return cls


class MonteCarloSampler_FunctionsTest(unittest.case.TestCase):

    def testConvertSamplesToRanks_empty(self):
        self.assertEqual(([], []), convertSamplesToRanks([], []))

    def testConvertSamplesToRanks_ints(self):
        x = [1, 4, 5]
        y = [0, 2, 3]
        self.assertEqual((x, y), convertSamplesToRanks(x, y))

    def testConvertSamplesToRanks_floats(self):
        x = [0.0, 1.5, 4.5, 5.5]
        y = [2.5, 3.5]
        self.assertEqual(([0,1,4,5], [2, 3]), convertSamplesToRanks(x, y))

    def testConvertSamplesToRanks_ties(self):
        x = [0.0, 1.5, 4.5, 5.5]
        y = [2.5, 3.5, 4.5, 4.5]
        self.assertEqual(([0,1,5,7], [2, 3, 5, 5]), convertSamplesToRanks(x, y))

    def testMeanDifference_empty(self):
        self.assertRaises(ZeroDivisionError, meanDifference, [], [])

    def testMeanDifference(self):
        self.assertEqual(5.25, meanDifference([-1,1,2,3], [5.5,7.5]))

    def testWilcoxonRankSum_empty(self):
        self.assertEqual(0, wilcoxonRankSum([], []))

    def testWilcoxonRankSum(self):
        self.assertEqual(12.5, wilcoxonRankSum([1,1,2,3], [5, 7.5]))


class MonteCarloEstimatorTest(unittest.case.TestCase):

    TEST_CLASS = MonteCarloEstimator

    def setUp(self):
        self.maxSamples = 50
        self.x = self.TEST_CLASS(self.maxSamples)

    def test__init__(self):
        self.assertIsInstance(self.TEST_CLASS(), self.TEST_CLASS)
        self.assertIsInstance(self.TEST_CLASS(maxSamples=10), self.TEST_CLASS)

    def test_finalizeEstimate(self):
        self.assertFalse(self.x._hasEstimate)
        self.x._finalizeEstimate()
        self.assertTrue(self.x._hasEstimate)

    def test_startEstimate(self):
        self.x._samples = 100
        self.x._estimate = 0.5
        self.x._finalizeEstimate()
        self.x._startEstimate()
        self.assertFalse(self.x._hasEstimate)
        self.assertEqual(0, self.x.getNumSamples())
        self.assertIsNone(self.x._estimate)

    def testAddSamples(self):
        self.assertRaises(NotImplementedError, self.x.addSamples, 10)
        self.x.getStatisticFunction = lambda : lambda sample : 0
        self.x.getSampleFunction = lambda : lambda : object()
        self.x.addSamples(10, False)
        self.assertEqual(10, self.x.getNumSamples())
        self.assertEqual(False, self.x._hasEstimate)
        self.x.addSamples(15, True)
        self.assertEqual(25, self.x.getNumSamples())
        self.assertEqual(True, self.x._hasEstimate)

    def testGetEstimate(self):
        self.x.getStatisticFunction = lambda : lambda sample : 0
        self.x.getSampleFunction = lambda : lambda : object()
        self.assertIsNone(self.x.getEstimate())

    def testGetNumSamples(self):
        self.assertEqual(self.x.getNumSamples(), 0)
        self.x.getStatisticFunction = lambda : lambda sample : 0
        self.x.getSampleFunction = lambda : lambda : object()
        self.x.addSamples(10)
        self.assertEqual(self.x.getNumSamples(), 10)

    def testGetStatisticFunction(self):
        self.assertRaises(NotImplementedError, self.x.getStatisticFunction)

    def testUpdateEstimate(self):
        self.x.getStatisticFunction = lambda : lambda sample : 0
        self.x.getSampleFunction = lambda : lambda : object()
        self.x.updateEstimate()
        self.assertEqual(self.x.getNumSamples(), self.maxSamples)
        


class MCHypothesisTestTest(unittest.case.TestCase):

    TEST_CLASS = MCHypothesisTest
    TEST_CLASS.VERBOSE = False
    TEST_CLASS = forceStaticSampling(TEST_CLASS)
    TEST_STATISTIC = staticmethod(lambda x, y: len(y))

    def setUp(self):
        self.sample1 = [1, 2, 3, 4]
        self.sample2 = [4, 5, 6.5, 10, 11]
        self.alternative = TWO_SIDED_HYPOTHESIS
        self.maxSamples = 50
        self.x = self.TEST_CLASS(self.sample1, self.sample2, self.TEST_STATISTIC,
                                 self.alternative, self.maxSamples)
                                 
    def test__init__(self):
        self.assertIsInstance(self.TEST_CLASS([1],[2], meanDifference), self.TEST_CLASS)
        self.assertIsInstance(self.TEST_CLASS([1],[2], meanDifference,
                                              alternative=TWO_SIDED_HYPOTHESIS, maxSamples=10),
                                              self.TEST_CLASS)
        self.assertRaises(ValueError, self.TEST_CLASS, [], [2], meanDifference)
        self.assertRaises(ValueError, self.TEST_CLASS, [1], [], meanDifference)
        self.assertRaises(ValueError, self.TEST_CLASS, [], [], meanDifference)
        self.assertRaises(ValueError, self.TEST_CLASS, [1], [2], meanDifference, alternative=4)

    def test_startEstimate(self):
        self.x._samples = 100
        self.x._estimate = 0.5
        self.x._count = 50
        self.x._tieCount = 20
        self.x._finalizeEstimate()
        self.x._startEstimate()
        self.assertFalse(self.x._hasEstimate)
        self.assertEqual(0, self.x.getNumSamples())
        self.assertIsNone(self.x._estimate)
        self.assertEqual(0, self.x._count)
        self.assertEqual(0, self.x._tieCount)

    def test_finalizeEstimate(self):
        self.assertFalse(self.x._hasEstimate)
        # Finalize with no samples
        self.x._finalizeEstimate()
        self.assertTrue(self.x._hasEstimate)
        self.assertIsNone(self.x._estimate)
        # Finalize with Dummy Data
        self.x._samples = 100
        self.x._count = 25
        self.x._tieCount = 5
        self.x._finalizeEstimate()
        self.assertEqual(0.6, self.x._estimate)

    def testAddSamples(self):
        self.x.addSamples(10, False)
        self.assertEqual(10, self.x.getNumSamples())
        self.assertEqual(False, self.x._hasEstimate)
        self.x.addSamples(15, True)
        self.assertEqual(25, self.x.getNumSamples())
        self.assertEqual(True, self.x._hasEstimate)
        self.assertEqual(0, self.x._count)
        self.assertEqual(25, self.x._tieCount)

    def testGetEstimate(self):
        self.assertEqual(1.0, self.x.getEstimate())

    def testGetNumSamples(self):
        self.assertEqual(self.x.getNumSamples(), 0)
        self.x.addSamples(10)
        self.assertEqual(self.x.getNumSamples(), 10)

    def testGetStatisticFunction(self):
        self.assertTrue(hasattr(self.x.getStatisticFunction, '__call__'))
        f = self.x.getStatisticFunction()
        self.assertEqual(0, f(self.sample1 + self.sample2))
        self.assertEqual(0, f(self.sample2 + self.sample1))

    def testUpdateEstimate(self):
        self.x.updateEstimate()
        self.assertEqual(self.x.getNumSamples(), self.maxSamples)
        self.assertTrue(self.x._hasEstimate)


class MCBStoppingRuleTestTest(MCHypothesisTestTest):

    TEST_CLASS = MCBStoppingRuleTest
    TEST_CLASS = forceStaticSampling(TEST_CLASS)
    TEST_CLASS.VERBOSE = False

    def setUp(self):
        self.sample1 = [1, 2, 3, 4]
        self.sample2 = [4, 5, 6.5, 10, 11]
        self.alternative = TWO_SIDED_HYPOTHESIS
        self.maxSamples = 100
        self.x = self.TEST_CLASS(self.sample1, self.sample2, self.TEST_STATISTIC,
                                 self.alternative, self.maxSamples)
                                 
    def test__init__(self):
        self.assertIsInstance(self.TEST_CLASS([1],[2], meanDifference), self.TEST_CLASS)
        self.assertIsInstance(self.TEST_CLASS([1],[2], meanDifference,
                                              alternative=TWO_SIDED_HYPOTHESIS, maxSamples=10,
                                              pValue = 0.9, upperBuffer=2.0, lowerBuffer=-1.0),
                                              self.TEST_CLASS)
        self.assertRaises(ValueError, self.TEST_CLASS, [], [2], meanDifference)
        self.assertRaises(ValueError, self.TEST_CLASS, [1], [], meanDifference)
        self.assertRaises(ValueError, self.TEST_CLASS, [], [], meanDifference)

    def test_startEstimate(self):
        self.x._samples = 100
        self.x._estimate = 0.5
        self.x._count = 50
        self.x._tieCount = 20
        self.x._boundHit = self.x.UPPER_BOUND_NAME
        self.x._finalizeEstimate()
        self.x._startEstimate()
        self.assertFalse(self.x._hasEstimate)
        self.assertEqual(0, self.x.getNumSamples())
        self.assertIsNone(self.x._estimate)
        self.assertEqual(0, self.x._count)
        self.assertEqual(0, self.x._tieCount)
        self.assertIsNone(self.x._boundHit)

    def test_updateBoundHit(self):
        scalingFactor = 1
        p = 1 - (1-self.x._pValue)/2.0
        self.x._maxSamples = 100*scalingFactor
        self.x._samples = 100*scalingFactor
        # Hits the Upper Bound (After updating)
        self.x._count = 79*scalingFactor
        self.x._tieCount = 20*scalingFactor
        self.assertIsNone(self.x._boundHit)
        self.x._updateBoundHit()
        self.assertEqual(self.x.UPPER_BOUND_NAME, self.x._boundHit)
        # Terminates without hitting a bound (in upper band)
        self.x._count = 98*scalingFactor
        self.x._tieCount = 0*scalingFactor
        self.x._updateBoundHit()
        self.assertIsNone(self.x._boundHit)
        # Hits the Inner Bound
        self.x._count = 45*scalingFactor
        self.x._tieCount = 5*scalingFactor
        self.x._updateBoundHit()
        self.assertEqual(self.x.INNER_BOUND_NAME, self.x._boundHit)
        # Terminates without hitting a bound (in lower band)
        self.x._count = 2*scalingFactor
        self.x._tieCount = 0*scalingFactor
        self.x._updateBoundHit()
        self.assertIsNone(self.x._boundHit)
        # Hits the Lower Bound (But classified as upper due to rectifying)
        self.x._count = 1*scalingFactor
        self.x._tieCount = 1*scalingFactor
        self.x._updateBoundHit()
        self.assertEqual(self.x.UPPER_BOUND_NAME, self.x._boundHit)

    def test_calculateBoundHit_TWO_SIDED(self):
        scalingFactor = 1
        p = 0.95
        # Hits the Upper Bound (After updating)
        bound = self.x._calculateBoundHit(79, 20, p, 100, 100, TWO_SIDED_HYPOTHESIS)
        self.assertEqual(self.x.UPPER_BOUND_NAME, bound)
        # Terminates without hitting a bound (in upper band)
        bound = self.x._calculateBoundHit(98, 0, p, 100, 100, TWO_SIDED_HYPOTHESIS)
        self.assertIsNone(bound)
        # Hits the Inner Bound
        bound = self.x._calculateBoundHit(45, 5, p, 100, 100, TWO_SIDED_HYPOTHESIS)
        self.assertEqual(self.x.INNER_BOUND_NAME, bound)
        # Terminates without hitting a bound (in lower band)
        bound = self.x._calculateBoundHit(2, 0, p, 100, 100, TWO_SIDED_HYPOTHESIS)
        self.assertIsNone(bound)
        # Hits the Lower Bound (But classified as upper due to rectifying)
        bound = self.x._calculateBoundHit(1, 0, p, 100, 100, TWO_SIDED_HYPOTHESIS)
        self.assertEqual(self.x.UPPER_BOUND_NAME, bound)

    def testIsBoundHit(self):
        self.assertFalse(self.x.isBoundHit(False))
        self.assertFalse(self.x.isBoundHit(True))
        self.x._samples = 100
        self.x._count = 79
        self.x._tieCount = 20
        self.assertFalse(self.x.isBoundHit(False))
        self.assertTrue(self.x.isBoundHit(True))
        self.assertTrue(self.x.isBoundHit(False))

    def testGetBoundHit(self):
        self.assertIsNone(self.x.getBoundHit(False))
        self.assertIsNone(self.x.getBoundHit(True))
        self.x._samples = 100
        self.x._count = 79
        self.x._tieCount = 20
        self.assertIsNone(self.x.getBoundHit(False))
        self.assertEqual(self.x.UPPER_BOUND_NAME, self.x.getBoundHit(True))
        self.assertEqual(self.x.UPPER_BOUND_NAME, self.x.getBoundHit(False))

    def testGetLowerBound(self):
        # 100 Sample Max
        self.assertEqual(90, self.x.getLowerBound(0.95, 100, 96))
        self.assertEqual(91, self.x.getLowerBound(0.95, 100, 97))
        self.assertEqual(94, self.x.getLowerBound(0.95, 100, 100))
        # 500 Sample Max
        self.assertEqual(80, self.x.getLowerBound(0.95, 500, 96))
        self.assertEqual(216, self.x.getLowerBound(0.95, 500, 239))
        self.assertEqual(474, self.x.getLowerBound(0.95, 500, 500))

    def testGetUpperBound(self):
        # 100 Sample Max
        self.assertEqual(96, self.x.getUpperBound(0.95, 100, 96))
        self.assertEqual(96, self.x.getUpperBound(0.95, 100, 97))
        self.assertEqual(96, self.x.getUpperBound(0.95, 100, 100))
        # 500 Sample Max
        self.assertEqual(103, self.x.getUpperBound(0.95, 500, 96))
        self.assertEqual(238, self.x.getUpperBound(0.95, 500, 239))
        self.assertEqual(476, self.x.getUpperBound(0.95, 500, 500))
    
    def testAddSamples(self):
        self.x.addSamples(10, False)
        self.assertEqual(10, self.x.getNumSamples())
        self.assertEqual(False, self.x._hasEstimate)
        self.x.addSamples(15, True)
        self.assertEqual(25, self.x.getNumSamples())
        self.assertEqual(True, self.x._hasEstimate)
        self.assertEqual(0, self.x._count)
        self.assertEqual(25, self.x._tieCount)
        self.x.addSamples(75, True)
        self.assertEqual(99, self.x.getNumSamples())
        self.assertEqual(0, self.x._count)
        self.assertEqual(99, self.x._tieCount)

    def testUpdateEstimate(self):
        self.x.updateEstimate()
        self.assertTrue(self.x.getNumSamples() <= self.maxSamples)
        self.assertTrue(self.x._hasEstimate)


class MCMeanDifferenceTestTest(MCHypothesisTestTest):
    TEST_CLASS = MCMeanDifferenceTest
    TEST_CLASS.VERBOSE = False
    TEST_CLASS = forceStaticSampling(TEST_CLASS)
    TEST_STATISTIC = meanDifference

    N_SAMPLES = 100
    MAX_SAMPLES = 1000
    # Groups of Distributions with same Mean+Median
    LOW_DISTRIBUTIONS = (('uniform', -0.5, 0.5),
                         ('choice', tuple([i/10.0 for i in xrange(-5,6)])),
                         ('gauss', 0, 1.0),
                         #(cauchy, 0.25, 1.0),
                         ('gauss', 0.0, 0.5))
    
    MID_DISTRIBUTIONS = (('uniform', 0.0, 1.0),
                         ('choice', tuple([i/10.0 for i in xrange(1,10)])),
                         ('gauss', 0.5, 1.0),
                         #(cauchy, 0.5, 1.0),
                         ('gauss', 0.5, 0.5))

    BIG_DISTRIBUTIONS = (('uniform', 1.0, 1.5),
                         ('choice', tuple([i/10.0 for i in xrange(11,20)])),
                         ('gauss', 1.5, 1.0),
                         #(cauchy, 1.5, 1.0),
                         ('gauss', 1.5, 0.5))

    def setUp(self):
        self.random = Random(1000)
        self.sample1 = [1, 2, 3, 4]
        self.bigSample1 = [100, 20, 3, 4]
        self.sample2 = [4, 5, 6.5, 10, 11]
        self.bigSample2 = [400, 500, 6.5, 100, 11]
        self.alternative = TWO_SIDED_HYPOTHESIS
        self.maxSamples = 20000
        self.x = self.TEST_CLASS(self.sample1, self.sample2, self.alternative, self.maxSamples)

    def _rand(self, distrName, *args):
        distr = getattr(self.random, distrName)
        return distr(*args)
                                 
    def test__init__(self):
        self.assertIsInstance(self.TEST_CLASS([1],[2]), self.TEST_CLASS)
        self.assertIsInstance(self.TEST_CLASS([1],[2], alternative=TWO_SIDED_HYPOTHESIS,
                                              maxSamples=10),
                                              self.TEST_CLASS)
        self.assertRaises(ValueError, self.TEST_CLASS, [], [2])
        self.assertRaises(ValueError, self.TEST_CLASS, [1], [])
        self.assertRaises(ValueError, self.TEST_CLASS, [], [])

    def testAddSamples(self):
        self.x.addSamples(10, False)
        self.assertEqual(10, self.x.getNumSamples())
        self.assertEqual(False, self.x._hasEstimate)
        self.x.addSamples(15, True)
        self.assertEqual(25, self.x.getNumSamples())
        self.assertEqual(True, self.x._hasEstimate)

    def testGetEstimate(self):
        mc = self.x
        self.assertTrue(mc.getEstimate() < 0.055)

    def testGetEstimate_Greater(self):
        mc = self.TEST_CLASS(self.sample1, self.sample2, GREATER_THAN_HYPOTHESIS, self.maxSamples)
        self.assertTrue(mc.getEstimate() > 0.95)

    def testGetEstimate_Less(self):
        mc = self.TEST_CLASS(self.sample1, self.sample2, LESS_THAN_HYPOTHESIS, self.maxSamples)
        self.assertTrue(mc.getEstimate() < 0.05) 

    def testGetStatisticFunction(self):
        self.assertTrue(hasattr(self.x.getStatisticFunction, '__call__'))
        f = self.x.getStatisticFunction()
        self.assertEqual(1, f(self.sample1 + self.bigSample2))
        self.assertEqual(0, f(self.sample1 + self.sample2))
        self.assertEqual(-1, f(self.bigSample1  + self.sample2))
        self.assertEqual(-1, f(self.sample2 + self.sample1))

    def testGetEstimate_AllLow(self):
        maxSamples = self.MAX_SAMPLES
        samples1 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                    for x in self.LOW_DISTRIBUTIONS]
        samples2 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                    for x in self.LOW_DISTRIBUTIONS]
        for val, alternative in [(False, TWO_SIDED_HYPOTHESIS),
                                 (False, GREATER_THAN_HYPOTHESIS),
                                 (False, LESS_THAN_HYPOTHESIS)]:
            for i, sample1 in enumerate(samples1):
                for j, sample2 in enumerate(samples2):
                    if i == j:
                        mc = self.TEST_CLASS(sample1, sample2, alternative, maxSamples)
                        #print i, j, alternative, mc.getEstimate()
                        self.assertEqual(val, mc.getEstimate() < 0.05)
                       
    def testGetEstimate_AllMid(self):
        maxSamples = self.MAX_SAMPLES
        samples1 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                    for x in self.MID_DISTRIBUTIONS]
        samples2 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                    for x in self.MID_DISTRIBUTIONS]
        for val, alternative in [(False, TWO_SIDED_HYPOTHESIS),
                                 (False, GREATER_THAN_HYPOTHESIS),
                                 (False, LESS_THAN_HYPOTHESIS)]:
            for i, sample1 in enumerate(samples1):
                for j, sample2 in enumerate(samples2):
                    if i == j:
                        mc = self.TEST_CLASS(sample1, sample2, alternative, maxSamples)
                        #print i, j, alternative, mc.getEstimate()
                        self.assertEqual(val, mc.getEstimate() < 0.05)

    def testGetEstimate_AllBig(self):
        maxSamples = self.MAX_SAMPLES
        samples1 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                    for x in self.BIG_DISTRIBUTIONS]
        samples2 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                    for x in self.BIG_DISTRIBUTIONS]
        for val, alternative in [(False, TWO_SIDED_HYPOTHESIS),
                                 (False, GREATER_THAN_HYPOTHESIS),
                                 (False, LESS_THAN_HYPOTHESIS)]:
            for i, sample1 in enumerate(samples1):
                for j, sample2 in enumerate(samples2):
                    if i == j:
                        mc = self.TEST_CLASS(sample1, sample2, alternative, maxSamples)
                        #print i, j, alternative, mc.getEstimate()
                        self.assertEqual(val, mc.getEstimate() < 0.05)

    def testGetEstimate_LowAndMid(self):
        maxSamples = self.MAX_SAMPLES
        samples1 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                     for x in self.LOW_DISTRIBUTIONS]
        samples2 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                     for x in self.MID_DISTRIBUTIONS]
        for val, alternative in [(True, TWO_SIDED_HYPOTHESIS),
                                 (False, GREATER_THAN_HYPOTHESIS),
                                 (True, LESS_THAN_HYPOTHESIS)]:
            for i, sample1 in enumerate(samples1):
                for j, sample2 in enumerate(samples2):
                        mc = self.TEST_CLASS(sample1, sample2, alternative, maxSamples)
                        #print i, j, alternative, mc.getEstimate()
                        self.assertEqual(val, mc.getEstimate() < 0.05)


    def testGetEstimate_MidAndBig(self):
        maxSamples = self.MAX_SAMPLES
        samples1 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                     for x in self.BIG_DISTRIBUTIONS]
        samples2 = [[self._rand(x[0], *x[1:]) for i in xrange(self.N_SAMPLES)]
                     for x in self.MID_DISTRIBUTIONS]
        for val, alternative in [(True, TWO_SIDED_HYPOTHESIS),
                                 (True, GREATER_THAN_HYPOTHESIS),
                                 (False, LESS_THAN_HYPOTHESIS)]:
            for i, sample1 in enumerate(samples1):
                for j, sample2 in enumerate(samples2):
                    mc = self.TEST_CLASS(sample1, sample2, alternative, maxSamples)
                    #print i, j, alternative, mc.getEstimate()
                    self.assertEqual(val, mc.getEstimate() < 0.05)


class MCWilcoxonRankTestTest(MCMeanDifferenceTestTest):
    TEST_CLASS = MCWilcoxonRankTest
    TEST_CLASS.VERBOSE = False
    TEST_CLASS = forceStaticSampling(TEST_CLASS)
    TEST_STATISTIC = wilcoxonRankSum
    IS_NON_PARAMETRIC = True

    def testGetStatisticFunction(self):
        self.assertTrue(hasattr(self.x.getStatisticFunction, '__call__'))
        f = self.x.getStatisticFunction()
        self.assertEqual(1, f(list.__add__(*convertSamplesToRanks(self.sample1, self.bigSample2))))
        self.assertEqual(0, f(list.__add__(*convertSamplesToRanks(self.sample1, self.sample2))))
        self.assertEqual(-1, f(list.__add__(*convertSamplesToRanks(self.sample2, self.sample1))))
        self.assertEqual(-1, f(list.__add__(*convertSamplesToRanks(self.bigSample1, self.sample2))))


class MCBMeanDifferenceTestTest(MCMeanDifferenceTestTest):
    TEST_CLASS = MCBMeanDifferenceTest
    TEST_CLASS.VERBOSE = False
    TEST_CLASS = forceStaticSampling(TEST_CLASS)
    TEST_STATISTIC = meanDifference
    IS_NON_PARAMETRIC = False
    MAX_SAMPLES = 20000

    def testUpdateEstimate(self):
        self.x.updateEstimate()
        self.assertTrue(self.x.getNumSamples() <= self.maxSamples)
        self.assertTrue(self.x._hasEstimate)

class MCBWilcoxonRankTestTest(MCWilcoxonRankTestTest):
    TEST_CLASS = MCBWilcoxonRankTest
    TEST_CLASS.VERBOSE = False
    TEST_CLASS = forceStaticSampling(TEST_CLASS)
    TEST_STATISTIC = wilcoxonRankSum
    IS_NON_PARAMETRIC = True
    MAX_SAMPLES = 20000

    def testUpdateEstimate(self):
        self.x.updateEstimate()
        self.assertTrue(self.x.getNumSamples() <= self.maxSamples)
        self.assertTrue(self.x._hasEstimate)


if __name__ == "__main__":
    unittest.main()
else:
    import sys
    TestSuite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
