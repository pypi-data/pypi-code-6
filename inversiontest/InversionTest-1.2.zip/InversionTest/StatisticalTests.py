"""
General statistical tests that operate on population samples,
such as the binomial test, sign test, and Wilcoxon signed rank test.
Also, contains relevant CDF, PMF, and PDF functions for related
distributions such as the binomial and normal distributions.

Note: If available, SciPy's optimized versions of binomial testing
and normal CDF calculations are utilized by default.  These should
be marginally faster, as they have hooks into C code.

Author: Benjamin D. Nye
License: Apache License V2.0
"""
import itertools
import random
from math import pi, erf, exp, floor, lgamma, log, sqrt, factorial
from InversionTest.Constants import (GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS,
                                     TWO_SIDED_HYPOTHESIS, TEST_HYPOTHESES)
from InversionTest.MonteCarloSampler import (MCBMeanDifferenceTest, MCBWilcoxonRankTest,
                                             MCMeanDifferenceTest, MCWilcoxonRankTest,
                                             meanDifference, convertSamplesToRanks)

# Optional Import of SciPy
try:
    import scipy.stats
    import scipy.stats.distributions
    IS_SCIPY_AVAILABLE = True
except ImportError:
    IS_SCIPY_AVAILABLE = False

SQRT_OF_TWO = sqrt(2.0)

# Exceptions
#----------------------------
class SignTestException(Exception): pass
class SignTestCancelationError(SignTestException): pass
class SignTestInvalidPairLengthError(SignTestException): pass

# Statistic Prototypes (Bound at End)
#-------------------------------
def binomialTest(x, n, p=0.5, alternative=TWO_SIDED_HYPOTHESIS):
    """
    Exact binomial test, where two-sided test uses a minlike formulation.
    This two-sided approach was chosen to match frameworks like R and SciPy.
    For reference, the minlike calculation is the sum of all p(k,n) where p(k,n)<=p(x,n)
    @param x: Number of successes
    @type x: int
    @param n: Number of observations
    @type n: int
    @param p: Assumed probability of a success, in [0,1]
    @type p: float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @return: Probability of the null hypothesis, in [0,1]
    @rtype: float
    """
    raise NotImplementedError

def signTest(series, series2=None, mu=0.0, alternative=TWO_SIDED_HYPOTHESIS):
    """
    A sign test, which works based on the counts that are greater or less
    than the compared pairs or null hypothesis mean.  Uses the binomial test
    with p=0.5 to calculate the probability.
    @param series: The series of values to test
    @type series: list of float
    @param series2: A series of comparison pairs, optionally.  If None, mu is used instead.
    @type series2: list of float or None
    @param mu: A comparison value to compare all values in series against (used only if series2 is None)
    @type mu: float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @return: Probability of the null hypothesis, in [0,1]
    @rtype: float
    """
    raise NotImplementedError

def wilcoxonSignedRankStatistic(series, series2=None, mu=0.0):
    """
    A Wilcoxon Signed Rank test statistic, for distributions symmetric around the median
    Returns the statistic value and the pValue
    @param series: A series of values
    @type series: list of float
    @param series2: A second series of values, optionally (if None, mu is used instead)
    @type series2: list of float or None
    @param mu: The presumed median for values (used only if y is None)
    @type mu: float
    @return: Probability of the null hypothesis, given the alternative
    @rtype: float
    """
    raise NotImplementedError

# Statistic Tests
#-----------------------------
def permutationTest(x, y, funct, alternative=TWO_SIDED_HYPOTHESIS):
    """
    A generic permutation hypothesis test between two sample populations.
    Runs all permutations of funct(x',y') where x' and y' are generated
    from the data points in x and y, then finds where funct(x,y) falls
    into the generated distribution.
    NOTE: This is crushingly slow as len(x) + len(y) > 10.  A Monte Carlo
    or partial-coverage permutation test is recommended for larger N.
    @param x: First sample set of data points
    @type x: list of float
    @param y: Second sample set of data points
    @type y: list of float
    @param funct: Statistic function, in form funct(x, y)
    @type funct: callable
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @return: Probability of the null hypothesis, given the alternative
    @rtype: float
    """
    nX = len(x)
    vObs = funct(x, y)
    if alternative == GREATER_THAN_HYPOTHESIS:
        counter = 0
        for z in itertools.permutations(list(x)+list(y)):
            if funct(z[:nX], z[nX:]) <= vObs:
                 counter += 1
        pValue = counter/float(factorial(len(x)+len(y)))
    elif alternative == LESS_THAN_HYPOTHESIS:
        counter = 0
        for z in itertools.permutations(list(x)+list(y)):
            if funct(z[:nX], z[nX:]) >= vObs:
                counter += 1
        pValue = counter/float(factorial(len(x)+len(y)))
    else:
        counter = 0
        tieCounter = 0
        for z in itertools.permutations(list(x)+list(y)):
            val = funct(z[:nX], z[nX:]) 
            if val < vObs:
                counter += 1
            elif val == vObs:
                tieCounter += 1
        nSamples = factorial(len(x) + len(y))
        cValue = counter/float(nSamples)
        tieValue = tieCounter/float(nSamples)
        pValue = 2.0*min(cValue+tieValue, 1-cValue)
    return min(1.0, pValue)

def permutationMeanTest(x, y, alternative=TWO_SIDED_HYPOTHESIS,
                        pValue=0.99, iterations=100000, useStoppingRule=True, maxExactN=7):
    """
    Permutation test that tests for differences in the means of two samples
    (e.g., a two-sample t-like statistic of mean(s1)-mean(s2)).
    If nToApprox is defined, this sets a cutoff for exact estimation after
    which a Monte Carlo approximation is used instead.
    @param x: First sample set of data points
    @type x: list of float
    @param y: Second sample set of data points
    @type y: list of float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @param pValue: The p-Value for the test to confirm, used for Monte Carlo early termination
    @type pValue: float
    @param iterations: The max number of iterations to run for Monte Carlo
    @type iterations: int
    @param useStoppingRule: If True, use version of MonteCarlo with an unbiased early stopping rule
    @type useStoppingRule: bool 
    @param maxExactN: The largest N=len(x)+len(y) to calculate an exact test value.
                      For values higher than this, use a Monte Carlo approximation.
    @type maxExactN: int
    @return: Probability of the null hypothesis, given the alternative
    @rtype: float
    """
    if maxExactN is None or (len(x) + len(y) <= maxExactN):
        return permutationTest(x, y, meanDifference, alternative)
    elif useStoppingRule:
        return MCBMeanDifferenceTest(x, y, alternative, iterations, pValue).getEstimate()
    else:
        return MCMeanDifferenceTest(x, y, alternative, iterations).getEstimate()

def permutationRankTest(x, y, alternative=TWO_SIDED_HYPOTHESIS,
                        pValue=0.99, iterations=100000, useStoppingRule=True, maxExactN=7):
    """
    Permutation test that tests for differences in the ranks of two samples.
    @param x: First sample set of data points
    @type x: list of float
    @param y: Second sample set of data points
    @type y: list of float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @param pValue: The p-Value for the test to confirm, used for Monte Carlo early termination
    @type pValue: float
    @param iterations: The max number of iterations to run for Monte Carlo
    @type iterations: int
    @param useStoppingRule: If True, use version of MonteCarlo with an unbiased early stopping rule
    @type useStoppingRule: bool
    @param maxExactN: The largest N=len(x)+len(y) to calculate an exact test value.
                      For values higher than this, use a Monte Carlo approximation.
    @type maxExactN: int
    @return: Probability of the null hypothesis, given the alternative    
    @rtype: float
    """
    if maxExactN is None or (len(x) + len(y) <= maxExactN):
        x, y = convertSamplesToRanks(x, y)
        def simpleWStat(x, y):
            return sum(y)
        return permutationTest(x, y, simpleWStat, alternative)
    elif useStoppingRule:
        return MCBWilcoxonRankTest(x, y, alternative, iterations, pValue).getEstimate()
    else:
        return MCWilcoxonRankTest(x, y, alternative, iterations).getEstimate()
        

def wilcoxonSignedRankTest(x, y=None, mu=0.0, alternative=TWO_SIDED_HYPOTHESIS):
    """
    A Wilcoxon Signed Rank test, for distributions symmetric around the median
    @param x: A series of values
    @type x: list of float
    @param y: A second series of values, optionally (if None, mu is used instead)
    @type y: list of float or None
    @param mu: The presumed median for values (used only if y is None)
    @type mu: float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @return: Probability of the null hypothesis, given the alternative
    @rtype: float
    """
    wStat, pValue = wilcoxonSignedRankStatistic(x, y, mu)
    if alternative != TWO_SIDED_HYPOTHESIS:
        mean = wilcoxonMeanScore(x, y, mu)
        transform = transformSymmetricPValueHypothesis
        pValue = transform(mean-wStat, pValue, TWO_SIDED_HYPOTHESIS, alternative)
    return pValue

# Test Statistic Built-In Implementations
#--------------------------------
def pythonBinomialTest(x, n, p=0.5, alternative=TWO_SIDED_HYPOTHESIS, useMinlike=True):
    """
    Exact binomial test, where two-sided test uses a minlike formulation.
    This two-sided approach was chosen to match frameworks like R and SciPy.
    For reference, the minlike calculation is the sum of all p(k,n) where p(k,n)<=p(x,n)
    @param x: Number of successes
    @type x: int
    @param n: Number of observations
    @type n: int
    @param p: Assumed probability of a success, in [0,1]
    @type p: float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @param useMinlike: If True, calculate a minlike two-tail.  Else, return 2*min(p_low, p_high).
    @type useMinlike: bool
    @return: Probability of the null hypothesis, in [0,1]
    @rtype: float
    """
    x = int(floor(x))
    n = int(floor(n))
    # One-Sided Cases
    if alternative == GREATER_THAN_HYPOTHESIS:
        if x == 0:
            pValue = 1.0
        else:
            pValue = 1.0-binomialCDF(max(0,x-1), n, p)
    elif alternative == LESS_THAN_HYPOTHESIS:
        pValue = binomialCDF(x, n, p)
    # Two-sided cases
    elif x == n*p:
        pValue = 1.0
    elif useMinlike:
        # Expand to two-tailed using min-like 
        if x > n*p:
            x = n-x
            p = 1-p
        tail1 = binomialCDF(x, n, p)
        tail2 = 0
        pStop = binomialPMF(x, n, p)
        for k in xrange(0, int(floor(n*p))):
            pmfVal = binomialPMF(n-k, n, p)
            if pmfVal > pStop:
                break
            else:
                tail2 += pmfVal
        pValue = tail1 + tail2
    else:
        # Use minimum-based two-tail formulation
        pValue = 2.0*min(pythonBinomialTest(x,n,p, LESS_THAN_HYPOTHESIS),
                         pythonBinomialTest(x,n,p, GREATER_THAN_HYPOTHESIS))
    return max(0.0, min(1.0, pValue))

def pythonSignTestStatistic(series, series2=None, mu=0.0, alternative=TWO_SIDED_HYPOTHESIS):
    """
    A sign test, which works based on the counts that are greater or less
    than the compared pairs or null hypothesis mean.  Uses the binomial test
    with p=0.5 to calculate the probability.
    @param series: The series of values to test
    @type series: list of float
    @param series2: A series of comparison pairs, optionally.  If None, mu is used instead.
    @type series2: list of float or None
    @param mu: A comparison value to compare all values in series against (used only if series2 is None)
    @type mu: float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @return: Probability of the null hypothesis, in [0,1]
    @rtype: float
    """
    if series2:
        if len(series) != len(series2):
            raise SignTestInvalidPairLengthError("Sign test requires series of equal length")
        signCount = [series2[i] < series[i] for i in xrange(len(series)) if series[i] != series2[i]]
    else:
        signCount = [mu < series[i] for i in xrange(len(series)) if series[i] != mu]
    n = len(signCount)
    x = sum(signCount)
    if n == 0:
        raise SignTestCancelationError("All terms in sign test canceled out, test invalid.")
    pValue = binomialTest(x, n, 0.5, alternative)
    return pValue

def pythonWilcoxonSignedRankStatistic(series, series2=None, mu=0.0):
    """
    A Wilcoxon two-sided test.  This uses a normal approximation and
    adjusts for ties using a variance penalty of (t^3-t)/48.0 for each
    tie of length t.
    @param series: A series of values
    @type series: list of float
    @param series2: A second series of values, optionally (if None, mu is used instead)
    @type series2: list of float or None
    @param mu: The presumed median for values (used only if y is None)
    @type mu: float
    @return: Wilcoxon statistic value (W+), Probability of the null hypothesis
    @rtype: float, float
    """
    # Calculate differences
    if series2:
        if len(series) != len(series2):
            raise IndexError("Wilcoxon Signed Rank test requires series of equal length")
        diffs = [series2[i]-series[i] for i in xrange(len(series))
                 if series2[i]-series[i] != 0]
    else:
        diffs = [mu-series[i] for i in xrange(len(series))
                 if mu-series[i] != 0]
    N = len(diffs)
    ties = []
    wRankSum = 0
    rank = 1
    # Group by absolute value ranks and iterate over groups to calculate W+
    diffs.sort(key=absAndValKey)
    for val, group in itertools.groupby(diffs, abs):
        group = [x for x in group]
        numItems = len(group)
        if numItems > 1:
            ties.append(numItems)
        value = (rank + (numItems-1)/2.0)
        wRankSum += value*len([x for x in group if x < 0])
        rank += numItems
    # Calculate p-value using a normal approximation
    mean = N*(N+1)/4.0
    variance = N*(N+1)*(2*N+1)/24.0 - sum([(t**3-t)/48.0 for t in ties])
    minWRank = min(wRankSum, N*(N+1)/2.0 - wRankSum)
    zScore = (minWRank-mean)/sqrt(variance)
    cdfValue = normalCDFFunction(-abs(zScore), 0.0, 1.0)
    pValue = 2.0*cdfValue
    return wRankSum, pValue

def wilcoxonMeanScore(series, series2=None, mu=0.0):
    """
    Get the mean Wilcoxon score, given equality
    @param series: A series of values
    @type series: list of float
    @param series2: A second series of values, optionally (if None, mu is used instead)
    @type series2: list of float or None
    @param mu: The presumed median for values (used only if y is None)
    @type mu: float
    @return: Mean Wilcoxon statistic value
    @rtype: float, float
    """
    if series2:
        if len(series) != len(series2):
            raise IndexError("Wilcoxon Signed Rank test requires series of equal length")
        diffs = [series2[i]-series[i] for i in xrange(len(series))
                 if series2[i]-series[i] != 0]
    else:
        diffs = [mu-series[i] for i in xrange(len(series))
                 if mu-series[i] != 0]
    N = len(diffs)
    return N*(N+1)/4.0

# Test Statistic SciPy Implementations
#--------------------------------
def scipyBinomialTestStatistic(x, n, p=0.5, alternative=TWO_SIDED_HYPOTHESIS):
    """
    Wrapper for the SciPy binomial two-sided test and binomial CDF calculations
    for one-tailed tests.  This allows testing two-sided and both one-sided hypotheses.
    @param x: Number of successes
    @type x: int
    @param n: Number of observations
    @type n: int
    @param p: Assumed probability of a success, in [0,1]
    @type p: float
    @param alternative: The alternate hypothesis for this test, from TEST_HYPOTHESES set
    @type alternative: str
    @return: Probability of the null hypothesis, in [0,1]
    @rtype: float
    """
    if alternative == LESS_THAN_HYPOTHESIS:
        pValue = 1.0-scipy.stats.binom.sf(x, n, p)
    elif alternative == GREATER_THAN_HYPOTHESIS:
        pValue = 1.0-scipy.stats.binom.cdf(max(0,x-1), n, p)
    else:
        pValue = scipy.stats.binom_test(x, n, p)
    return pValue

def scipyWilcoxonStatistic(series, series2=None, mu=0.0):
    """
    The SciPy Wilcoxon two-sided test.  This test always uses
    a normal approximation and does not adjust for ties properly,
    but should be (theoretically) faster than the pure python
    versions here, as it uses C code under the hood.
    @param series: A series of values
    @type series: list of float
    @param series2: A second series of values, optionally (if None, mu is used instead)
    @type series2: list of float or None
    @param mu: The presumed median for values (used only if y is None)
    @type mu: float
    @return: Wilcoxon statistic value of min(W+,W-), Probability of the null hypothesis
    @rtype: float, float
    """
    if series2 is None:
        series2 = [mu]*len(series)
    wStatistic, pValue = scipy.stats.wilcoxon(series, series2)
    return wStatistic, pValue

# Probability Distributions
#-----------------------------
def binomialPMF(x, n, p):
    """
    Binomial PMF, using log-gamma implementation
    @param x: # of successes
    @type x: int
    @param n: Number of observations
    @type n: int
    @param p: Probability of a success
    @type p: float
    @return: Point mass for x in the binomial distribution
    @rtype: float
    """
    return exp(lgamma(n+1) - lgamma(x+1) - lgamma(n-x+1) + x*log(p) + (n-x)*log(1-p))

def binomialCDF(x, n, p):
    """
    Binomial CDF, using log-gamma implementation
    @param x: # of successes
    @type x: int
    @param n: Number of observations
    @type n: int
    @param p: Probability of a success
    @type p: float
    @return: Cummulative distribution function for x in the binomial distribution
    @rtype: float
    """
    lnMaxFact = lgamma(n+1)
    q = 1.0-p
    pValue = 0.0
    if x <= n*p:
        for k in xrange(0, int(x+1)):
            pValue += exp(lnMaxFact - lgamma(k+1) - lgamma(n-k+1)
                          + k*log(p) + (n-k)*log(q))
    else:
        for k in xrange(int(x+1), n+1):
            pValue += exp(lnMaxFact - lgamma(k+1) - lgamma(n-k+1)
                          + k*log(p) + (n-k)*log(q))
        pValue = 1.0 - pValue
    return pValue

def binomialNormalApproximationHeuristic(n, p, threshold=0.30, minN=25):
    """
    A heuristic for when the normal approximation is reasonable
    @param n: Number of observations
    @type n: int
    @param p: Probability of a success
    @type p: float
    @param threshold: Threshold for the heuristic, in [0, 1] where 0 is never and 1 is always
    @type threshold: float
    @param minN: Minimum n to have before using the approximation under any circumstances
    @type minN: int
    @return: True (use normal distribution) if heuristic < threshold and n > minN, else False
    @rtype: bool
    """
    if n > minN:
        heuristic = abs((sqrt(p/(1-p)) - sqrt((1-p)/p))/sqrt(n))
        return heuristic < threshold
    else:
        return False

def pythonNormalCDF(x, loc=0.0, scale=1.0):
    """
    Normal CDF (Phi) implementation based on the error function in Python 2.7
    @param x: Value for CDF, x in P(X<=x) where X ~ N(mu=loc, var=scale**2)
    @type x: float
    @param loc: Location parameter (mean)
    @type loc: float
    @param scale: Scale parameter (variance)
    @type scale: float
    @return: CDF value from the normal distribution
    @rtype: float
    """
    x = (x-loc)/float(scale)
    return 0.5 + 0.5*erf(x/SQRT_OF_TWO)

# Utility Functions
#-----------------------------
def absAndValKey(x):
    """
    Return the absolute value and the value of a number
    @param x: Some number
    @type x: int or float
    @return: abs(x), x
    @rtype: tuple of (int or float, int or float)
    """
    return abs(x), x

def genericSymmetricPairedTest(statistic, statisticAlternative, alternative, *args, **kwds):
    """
    Generic symmetric paired test, to convert between different-sided results
    @param statistic: A statistic function, in the form f(x, y, mu)
    @type statistic: callable
    @param statisticAlternative: The hypothesis for the test alternative, from TEST_HYPOTHESES set
    @type statisticAlternative: str
    @param args: Variable arguments, to pass to the statistic
    @type args: list of object
    @param kwds: Variable keyword arguments, to pass to the statistic
    @type kwds: dict of {str : object}
    """
    statisticValue, pValue = statistic(*args, **kwds)
    pValue = transformSymmetricPValueHypothesis(statisticValue, pValue, statisticAlternative, alternative)
    return pValue

def transformSymmetricPValueHypothesis(statisticVal, pValue, originalAlternative, newAlternative):
    """
    Transform a probability of one hypothesis into another hypothesis, assuming a symmetric
    distribution (such as a normal distribution).  This is used to convert from functions
    that return a statistic and pValue, but a different hypothesis must be examined.
    @param statisticVal: Value of the statistic (assumed that the CDF integrates from lowest to highest values)
    @type statisticVal: float
    @param pValue: Probability, as based on the original alternative for the statistic calculator
    @type pValue: float
    @param originalAlternative: The alternate hypothesis assumed by the test, from TEST_HYPOTHESES set
    @type originalAlternative: str
    @param newAlternative: The new alternate hypothesis to report a pValue for
    @type newAlternative: str
    @return: Adjusted pValue to reflect new alternative hypothesis
    @rtype: float
    """
    if originalAlternative == newAlternative:
        return pValue
    elif originalAlternative == TWO_SIDED_HYPOTHESIS:
        pValue = pValue/2.0
        if ((newAlternative == LESS_THAN_HYPOTHESIS and statisticVal < 0) or
            (newAlternative == GREATER_THAN_HYPOTHESIS and statisticVal > 0)):
            pValue = 1.0 - pValue
        return pValue
    elif newAlternative != TWO_SIDED_HYPOTHESIS:
        return 1.0 - pValue
    else:
        return min(pValue, 1.0-pValue)*2.0

# Utility Classes
#-----------------------------
class SystemReseededRandom(object):
    """
    Random number generator that randomly re-positions a standard MT
    generator based on the system random entropy generator, so that
    any permutation is theoretically possible.
    """
    RESET_COUNT = 2**1000
    MAX_SKIP = 2**100
    def __init__(self):
        """ Initialize the random number generators and reset counter"""
        self.count = 0
        self.rng = random.Random()
        self.sysRandom = random.SystemRandom()
        self.random = self.rng.random
        
    def random(self):
        """ Generate a random number """
        if self.count >= self.RESET_COUNT:
            self.count = 0
            self.rng.jumpahead(self.sysRandom.randrange(0,self.MAX_SKIP))
        self.count += 1
        return self.random()

# Public Test Implementations
#----------------------------
signTest = pythonSignTestStatistic                                  #Use native, as SciPy lacks
wilcoxonSignedRankStatistic = pythonWilcoxonSignedRankStatistic     #Use native, as SciPy bad on ties
if IS_SCIPY_AVAILABLE:
    # If SciPy is available, use its binomial and normal functions
    binomialTest = scipyBinomialTestStatistic
    normalCDFFunction = scipy.stats.norm.cdf
else:
    binomialTest = pythonBinomialTest
    normalCDFFunction = pythonNormalCDF
