import itertools
from math import ceil, floor
from random import shuffle
from InversionTest.Constants import (GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS,
                                     TWO_SIDED_HYPOTHESIS, TEST_HYPOTHESES)

class MonteCarloEstimator(object):
    """ A Monte Carlo Estimator """
    
    def __init__(self, maxSamples=10000):
        """
        Initialize the estimator
        @param maxSamples: Maximum number of samples to run for an estimate
        @type maxSamples: int
        """
        self._maxSamples = maxSamples
        self._samples = 0
        self._estimate = None
        self._hasEstimate = False

    def _startEstimate(self):
        """ Start the Monte Carlo estimate """
        self._hasEstimate = False
        self._estimate = None
        self._samples = 0
        
    def _updateSupport(self, statistic):
        """
        Update support based on the latest statistic value
        @param statistic: Value of the statistic for the most recent sample
        @type statistic: object
        """
        pass

    def _finalizeEstimate(self):
        """ Finalize the estimate """
        self._hasEstimate = True
    
    def getStatisticFunction(self):
        """
        Get the function that calculates a statistic from a sample
        @return: Function in form f(sample): return statistic
        @rtype: callable
        """
        raise NotImplementedError

    def getSampleFunction(self):
        """
        Return the sample function, which generates random samples
        @return: Sample generating function, in the form f(): return sample
        @rtype: callable
        """
        raise NotImplementedError

    def addSamples(self, n, finalize=True):
        """
        Add a maximum of n samples to the estimate
        @param n: Maximum number of samples to add
        @type n: int
        @param finalize: If True, finalize estimate value after adding samples
        @type finalize: bool
        """
        calcStatistic = self.getStatisticFunction()
        getSample = self.getSampleFunction()
        updateSupport = self._updateSupport
        for i in xrange(n):
            sample = getSample()
            statistic = calcStatistic(sample)
            updateSupport(statistic)
            self._samples += 1
        if finalize:
            self._finalizeEstimate()

    def getEstimate(self, update=False):
        """
        Get the value of the Monte Carlo estimate.
        If no estimate available, calculate an estimate
        @param update: If True, force re-calculation of the estimate.
        @type update: bool
        @return: Monte Carlo estimate
        @rtype: object
        """
        if not self._hasEstimate or update:
            self.updateEstimate()
        return self._estimate

    def getNumSamples(self):
        """
        Return the number of samples used in the estimate so far
        @return: Number of samples drawn for the Monte Carlo estimate
        @rtype: int
        """
        return self._samples

    def updateEstimate(self):
        """ Calculate and store the Monte Carlo estimate """
        self._startEstimate()
        self.addSamples(self._maxSamples, False)
        self._finalizeEstimate()


class MCHypothesisTest(MonteCarloEstimator):
    """ Monte Carlo Bernoulli Hypothesis Test """
    VERBOSE = True
    
    def __init__(self, sample1, sample2, testStatistic,
                 alternative=TWO_SIDED_HYPOTHESIS,
                 maxSamples=10000):
        """
        Initialize the estimator
        @param sample1: First sample of data points
        @type sample1: list of object
        @param sample2: Second sample of data points
        @type sample2: list of object
        @param testStatistic: Statistic function to run on each sample,
                              in the form f(sample): return statistic
        @type testStatistic: callable
        @param alternative: Alternate hypothesis, from the set GREATER_THAN_HYPOTHESIS,
                            LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        @type alternative: str
        @param maxSamples: Maximum number of samples to run for an estimate
        @type maxSamples: int
        """
        super(MCHypothesisTest, self).__init__(maxSamples)
        if len(sample1) == 0 or len(sample2) == 0:
            raise ValueError("MC Hypothesis Error: Both samples must have at least one element")
        if alternative not in TEST_HYPOTHESES:
            raise ValueError("MC Hypothesis Error: alternative was not a valid test hypothesis, got '%s', need %s"%(alternative, TEST_HYPOTHESES))
        if maxSamples <= 0:
            raise ValueError("MC Hypothesis Error: maxSamples was less than 1")
        elif maxSamples < 1000:
            if self.VERBOSE == True:
                print "Warning: Maximum samples for Monte Carlo was very low, got: %s"%(maxSamples,)
        
        self._sample1 = sample1
        self._sample2 = sample2
        self._testStatistic = testStatistic
        self._alternative = alternative
        self._count = 0
        self._tieCount = 0      # Count ties for two-tailed only
        self._combinedSample = list(sample1) + list(sample2)
    
    def _startEstimate(self):
        """ Start the Monte Carlo estimate """
        super(MCHypothesisTest, self)._startEstimate()
        self._count = 0
        self._tieCount = 0 
        
    def _updateSupport(self, statistic):
        """
        Update the count of samples where the alternate hypothesis was confirmed
        @param statistic: If sample confirms alternate value is 1, else value is 0
        @type statistic: int
        """
        if self._alternative == TWO_SIDED_HYPOTHESIS:
            if statistic > 0:
                self._count += 1
            elif statistic == 0:
                self._tieCount += 1
        else:
            self._count += statistic

    def _finalizeEstimate(self):
        """
        Finalize the estimate, which is the # positive samples divided by total samples
        """
        super(MCHypothesisTest, self)._finalizeEstimate()
        if self._samples == 0:
            self._estimate = None
        else:
            if self._alternative == TWO_SIDED_HYPOTHESIS:
                cValue = self._count/float(self._samples)
                tValue = self._tieCount/float(self._samples)
                val = 2.0*min(cValue + tValue, 1 - cValue)
            else:
                val = self._count/float(self._samples)
            self._estimate = min(1.0, val) 

    def getSampleFunction(self):
        """
        Return the sample function, which generates random samples
        @return: Sample generating function, in the form f(): return sample
        @rtype: callable
        """
        return self._sampleFunction

    def _sampleFunction(self):
        """
        Sample function for the estimator.  This shuffles the combined
        sample of sample1 + sample2, returning a random permutation.
        @return: Random permutation of the combined sample set
        @rtype: list of object
        """
        shuffle(self._combinedSample)
        return self._combinedSample
    
    def getStatisticFunction(self):
        """
        Get the statistic function for the estimator.
        This function calculates an indicator variable based on a sample
        as generated by getSampleFunction.
        @return: Statistic function in form f(sample): return bool
        @rtype: callable
        """
        alternative = self._alternative
        testStatistic = self._testStatistic
        vObs = testStatistic(self._sample1, self._sample2)
        n1 = len(self._sample1)
        if alternative == GREATER_THAN_HYPOTHESIS:
            def anIndicatorFunction(sample):
                return int(testStatistic(sample[:n1], sample[n1:]) <= vObs)
        elif alternative == LESS_THAN_HYPOTHESIS:
            def anIndicatorFunction(sample):
                return int(testStatistic(sample[:n1], sample[n1:]) >= vObs)
        else:
            def anIndicatorFunction(sample):
                val = testStatistic(sample[:n1],sample[n1:])
                if val > vObs:
                    return 1
                elif val < vObs:
                    return -1
                else:
                    return 0
        return anIndicatorFunction


class MCMeanDifferenceTest(MCHypothesisTest):
    """
    Hypothesis test for the difference between means
    Terminates after a fixed number of samples
    """

    def __init__(self, sample1, sample2,
                 alternative=TWO_SIDED_HYPOTHESIS, 
                 maxSamples=10000):
        """
        Initialize the estimator
        @param sample1: First sample of data points
        @type sample1: list of object
        @param sample2: Second sample of data points
        @type sample2: list of object
        @param alternative: Alternate hypothesis, from the set GREATER_THAN_HYPOTHESIS,
                            LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        @type alternative: str
        @param maxSamples: Maximum number of samples to run for an estimate
        @type maxSamples: int
        """
        super(MCMeanDifferenceTest, self).__init__(sample1, sample2,
                                                   meanDifference,
                                                   alternative,
                                                   maxSamples)


class MCWilcoxonRankTest(MCHypothesisTest):
    """
    Hypothesis test for the difference between means
    Terminates after a fixed number of samples
    """

    def __init__(self, sample1, sample2,
                 alternative=TWO_SIDED_HYPOTHESIS, 
                 maxSamples=10000):
        """
        Initialize the estimator
        Before initializing, convert data points to their ranks
        @param sample1: First sample of data points
        @type sample1: list of object
        @param sample2: Second sample of data points
        @type sample2: list of object
        @param alternative: Alternate hypothesis, from the set GREATER_THAN_HYPOTHESIS,
                            LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        @type alternative: str
        @param maxSamples: Maximum number of samples to run for an estimate
        @type maxSamples: int
        """
        sample1, sample2 = convertSamplesToRanks(sample1, sample2)
        super(MCWilcoxonRankTest, self).__init__(sample1, sample2,
                                             wilcoxonRankSum,
                                             alternative,
                                             maxSamples)
        

class MCBStoppingRuleTest(MCHypothesisTest):
    """
    Hypothesis test based on the MCB stopping rule (Kim 2010)
    Terminates when it hits bounds or when the maximal samples
    have been hit.  Estimates within approximately 0.001 at the
    bounds for alpha=0.95 or alpha=0.99.
    
    Upper Bounds:
    r_1 = pValue*(maxSamples+1)
    c1*((m*p*(1-p))**0.5) + n*p

    Lower Bounds:
    r_0 = (1-pValue)*(maxSamples+1))
    c2*((m*p*(1-p))**0.5) + n*p

    For clarity in code, c1 is referred to as upperBuffer and c2
    is referred to as lowerBuffer.  The default upper and lower
    buffer sizes are taken from Kim (2010)
    """
    UPPER_BOUND_NAME = 'Upper'
    LOWER_BOUND_NAME = 'Lower'
    INNER_BOUND_NAME = 'Inner'
    DEFAULT_P_VALUE = 0.05
    DEFAULT_UPPER_BUFFER =  2.241
    DEFAULT_LOWER_BUFFER = -DEFAULT_UPPER_BUFFER
    
    def __init__(self, sample1, sample2, testStatistic,
                 alternative=TWO_SIDED_HYPOTHESIS,
                 maxSamples=10000, pValue=DEFAULT_P_VALUE,
                 upperBuffer=DEFAULT_UPPER_BUFFER,
                 lowerBuffer=DEFAULT_LOWER_BUFFER):
        """
        Initialize the estimator
        @param sample1: First sample of data points
        @type sample1: list of object
        @param sample2: Second sample of data points
        @type sample2: list of object
        @param testStatistic: Statistic function to run on each sample,
                              in the form f(sample): return statistic
        @type testStatistic: callable
        @param alternative: Alternate hypothesis, from the set GREATER_THAN_HYPOTHESIS,
                            LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        @type alternative: str
        @param maxSamples: Maximum number of samples to run for an estimate
        @type maxSamples: int
        @param pValue: P-value (alpha) for the test, in (0,1) range
        @type pValue: float
        @param upperBuffer: Buffer width for upper bound (c1).  Should be positive.
                           Higher values require more positives to terminate early.
        @type upperBuffer: float
        @param lowerBuffer: Buffer width for the lower bound (c2).  Should be negative.
                            Higher absolute values require more negatives to terminate early.
        @type lowerBuffer: float
        """
        super(MCBStoppingRuleTest, self).__init__(sample1, sample2,
                                                  testStatistic,
                                                  alternative,
                                                  maxSamples)
        if alternative == TWO_SIDED_HYPOTHESIS:
            # Store the pValue as the upper
            pValue = max(pValue, 1.0-pValue)
        self._pValue = pValue
        self._upperBuffer = upperBuffer
        self._lowerBuffer = lowerBuffer
        self._boundHit = None

    def _updateBoundHit(self):
        """ Update which bound has been hit, if any """
        value = self._count
        tieCount = self._tieCount
        p = self._pValue
        m = self._maxSamples
        n = self._samples
        self._boundHit = self._calculateBoundHit(value, tieCount, p, m, n,
                                                 self._alternative)

    def _calculateBoundHit(self, value, tieCount, p, m, n, alternative):
        """
        Calculate which bound has been hit, if any
        @param value: The number of "hits" exceeding the observed value
        @type value: int
        @param tieCount: The number of ties equal to the observed value
        @type tieCount: int
        @param p: The p-value being tested, in [0, 1]
        @type p: float
        @param m: Max samples
        @type m: int
        @param n: Number of samples
        @type n: int
        @param alternative: Alternate hypothesis
        @type alternative: str
        @return: Bound hit
        @rtype: str or None
        """
        if alternative == TWO_SIDED_HYPOTHESIS:
            # Split p-value across the tails
            p = 1 - (1-p)/2.0
            highValue = max(value+tieCount, n-value)
            lowValue = min(value+tieCount, n-value)
            uBound = self.getUpperBound(p, m, n)
            lBound = self.getLowerBound(p, m, n)
            uBound2 = self.getUpperBound(1.0-p, m, n)
            if uBound is not None and highValue >= uBound:
                return self.UPPER_BOUND_NAME
            elif (lBound is not None and uBound2 is not None and
                  highValue <= lBound and 
                  lowValue > uBound2):
                return self.INNER_BOUND_NAME
            else:
                return None
        else:
            uBound = self.getUpperBound(p, m, n)
            lBound = self.getLowerBound(p, m, n)
            if uBound is not None and value >= uBound:
                return self.UPPER_BOUND_NAME
            elif lBound is not None and value <= lBound:
                return self.LOWER_BOUND_NAME
            else:
                return None

    def _startEstimate(self):
        """ Start the Monte Carlo estimate """
        super(MCBStoppingRuleTest, self)._startEstimate()
        self._boundHit = None

    def addSamples(self, n, finalize=True):
        """
        Add a maximum of n samples to the estimate.  If any
        termination bound hit, stop sampling and return.
        @param n: Maximum number of samples to add
        @type n: int
        @param finalize: If True, finalize estimate value after adding samples
        @type finalize: bool
        """
        calcStatistic = self.getStatisticFunction()
        getSample = self.getSampleFunction()
        updateSupport = self._updateSupport
        for i in xrange(n):
            sample = getSample()
            statistic = calcStatistic(sample)
            updateSupport(statistic)
            self._samples += 1
            if self.isBoundHit(update=True):
                break
        if finalize:
            self._finalizeEstimate()

    def isBoundHit(self, update=True):
        """
        Check if upper or lower bound has been hit.
        @param update: If True, update the stored value before returning
        @type update: bool
        @return: True if either bound hit, else False
        @rtype: bool
        """
        if update:
            self._updateBoundHit()
        return self._boundHit is not None

    def getBoundHit(self, update=True):
        """
        Get the boundary that has been crossed, if any.
        @param update: If True, update the stored value before returning
        @type update: bool
        @return: Return UPPER_BOUND_NAME if crossed the upper bound,
                 return LOWER_BOUND_NAME if crossed the lower bound,
                 return None if neither crossed
        @rtype: str
        """
        if update:
            self._updateBoundHit()
        return self._boundHit

    def getLowerBound(self, p, m, n):
        """
        Return the active lower bound for values
        @param p: Probability value for the test, in [0,1]
        @type p: float
        @param m: Maximum samples for the test
        @type m: int
        @param n: Number of samples so far in the test
        @param n: int
        @return: Lower bound value
        @rtype: int
        """
        bound = self._lowerBuffer*((m*p*(1-p))**0.5) + n*p
        r0 = (1-p)*(m+1)
        bound = max(floor(bound), floor(n-r0))
        if bound >= 0:
            return bound
        else:
            return None

    def getUpperBound(self, p, m, n):
        """
        Return the active upper bound value
        @param p: Probability value for the test, in [0,1]
        @type p: float
        @param m: Maximum samples for the test
        @type m: int
        @param n: Number of samples so far in the test
        @param n: int
        @return: Upper bound value
        @rtype: int
        """
        bound = self._upperBuffer*((m*p*(1-p))**0.5) + n*p
        r1 = p*(m+1)
        bound = min(ceil(bound), ceil(r1))
        if bound >= 0:
            return bound
        else:
            return None

class MCBMeanDifferenceTest(MCBStoppingRuleTest):
    """ Hypothesis test for the difference between means (e.g., like a t-Test) """
    DEFAULT_P_VALUE = MCBStoppingRuleTest.DEFAULT_P_VALUE
    DEFAULT_UPPER_BUFFER = MCBStoppingRuleTest.DEFAULT_UPPER_BUFFER
    DEFAULT_LOWER_BUFFER= MCBStoppingRuleTest.DEFAULT_LOWER_BUFFER
    
    def __init__(self, sample1, sample2,
                 alternative=TWO_SIDED_HYPOTHESIS,
                 maxSamples=10000, pValue=DEFAULT_P_VALUE,
                 upperBuffer=DEFAULT_UPPER_BUFFER,
                 lowerBuffer=DEFAULT_LOWER_BUFFER):
        """
        Initialize the estimator
        @param sample1: First sample of data points
        @type sample1: list of object
        @param sample2: Second sample of data points
        @type sample2: list of object
        @param alternative: Alternate hypothesis, from the set GREATER_THAN_HYPOTHESIS,
                            LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        @type alternative: str
        @param maxSamples: Maximum number of samples to run for an estimate
        @type maxSamples: int
        @param pValue: P-value (alpha) for the test, in (0,1) range
        @type pValue: float
        @param upperBuffer: Buffer width for upper bound (c1).  Should be positive.
                           Higher values require more positives to terminate early.
        @type upperBuffer: float
        @param lowerBuffer: Buffer width for the lower bound (c2).  Should be negative.
                            Higher absolute values require more negatives to terminate early.
        @type lowerBuffer: float
        """
        super(MCBMeanDifferenceTest, self).__init__(sample1, sample2,
                                                    meanDifference,
                                                    alternative, maxSamples,
                                                    pValue, upperBuffer, lowerBuffer)

class MCBWilcoxonRankTest(MCBStoppingRuleTest):
    """ Wilcoxon MC hypothesis test for the difference between location """
    DEFAULT_P_VALUE = MCBStoppingRuleTest.DEFAULT_P_VALUE
    DEFAULT_UPPER_BUFFER = MCBStoppingRuleTest.DEFAULT_UPPER_BUFFER
    DEFAULT_LOWER_BUFFER = MCBStoppingRuleTest.DEFAULT_LOWER_BUFFER
    
    def __init__(self, sample1, sample2,
                 alternative=TWO_SIDED_HYPOTHESIS,
                 maxSamples=10000, pValue=DEFAULT_P_VALUE,
                 upperBuffer=DEFAULT_UPPER_BUFFER,
                 lowerBuffer=DEFAULT_LOWER_BUFFER):
        """
        Initialize the estimator
        @param sample1: First sample of data points
        @type sample1: list of object
        @param sample2: Second sample of data points
        @type sample2: list of object
        @param alternative: Alternate hypothesis, from the set GREATER_THAN_HYPOTHESIS,
                            LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        @type alternative: str
        @param maxSamples: Maximum number of samples to run for an estimate
        @type maxSamples: int
        @param pValue: P-value (alpha) for the test, in (0,1) range
        @type pValue: float
        @param upperBuffer: Buffer width for upper bound (c1).  Should be positive.
                           Higher values require more positives to terminate early.
        @type upperBuffer: float
        @param lowerBuffer: Buffer width for the lower bound (c2).  Should be negative.
                            Higher absolute values require more negatives to terminate early.
        @type lowerBuffer: float
        """
        sample1, sample2 = convertSamplesToRanks(sample1, sample2)
        super(MCBWilcoxonRankTest, self).__init__(sample1, sample2,
                                                  wilcoxonRankSum,
                                                  alternative, maxSamples,
                                                  pValue, upperBuffer, lowerBuffer)


# Basic Statistics
def meanDifference(x, y):
    """
    Difference of means between x and y, i.e. avg(y) - avg(x)
    If either sample has zero elements, this raises an error
    @param x: First sample
    @type x: list of float
    @param y: Second sample
    @type y: list of float
    @return: Mean of y minus mean of x
    @rtype: float
    """
    return sum(y)/float(len(y)) - sum(x)/float(len(x))

def wilcoxonRankSum(x, y):
    """
    Sum of ranks of y
    If either sample has zero elements, this raises an error
    @param x: First sample
    @type x: list of float
    @param y: Second sample
    @type y: list of float
    @return: Sum of ranks of y
    @rtype: float
    """
    return sum(y)

# Utility Functions 
def convertSamplesToRanks(x, y):
    """
    Convert two sets of samples into their equivalent ranks
    For ranks that share the same value, average the range of
    ranks that they would hold.
    @param x: First sample
    @type x: list of float
    @param y: Second sample
    @type y: list of float
    @return: Tuple of (sample of x-ranks, sample of y-ranks)
    @rtype: list of float, list of float
    """
    dataRanks = [(val, 0) for val in x] + [(val, 1) for val in y]
    dataRanks.sort()
    newX = []
    newY = []
    n = 0
    extractGroupByValue = lambda x: x[0]
    for val, group in itertools.groupby(dataRanks, extractGroupByValue):
        group = list(group)
        numItems = len(group)
        rank = n + (numItems-1)/2.0
        for val, sampleId in group:
            if sampleId == 0:
                newX.append(rank)
            else:
                newY.append(rank)
        n += numItems
    return newX, newY

