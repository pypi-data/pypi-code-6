"""
Properties of the permutations (null distribution) for inversions
of a totally-ordered sequence.  Includes: max, mean, variance,
similarity, correlation, and counts of permutations with k inversions
(called I_n[k] in some literature).

Author: Benjamin D. Nye
License: Apache License V2.0
"""

# Basic Properties
#------------------------------------------
def maxInversions(n):
    """
    Maximum inversions for a permutation of a sequence of n elements
    Note: This will always return an integer
    @param n: Number of elements
    @type n: int
    @return: Maximum number of inversions between n elements
    @rtype: int
    """
    return (n*(n-1))/2

def meanOfInversions(n):
    """
    Mean (expected) inversions for a permutation of a sequence of n elements
    Note: This returns a float, as the expectation maybe fractional.
    @param n: Number of elements
    @type n: int
    @return: Mean number of inversions across all permutations
    @rtype: float
    """
    return (n*(n-1))/4.0

def varianceOfInversions(n):
    """
    Variance of inversions for a permutation of a sequence of n elements
    Note: This returns a float, as the variance maybe fractional.
    @param n: Number of elements
    @type n: int
    @return: Variance of inversions across all permutations
    @rtype: float
    """
    return (n*(n-1.0)*(2.0*n + 5.0))/72.0

def correlationByInversions(inversions, maxInversions):
    """
    Correlation between sequences, given the inversions and max possible
    A correlation of -1 is the worst, while 1 is the best.  This value
    is equivalent to a Kendall's Tau correlation.
    @param inversions: Number of inversions
    @type inversions: int
    @param maxInversions: Maximum possible inversions
    @type maxInversions: int
    @return: Correlation, in [-1, 1]
    @rtype: float
    """
    sim = similarityByInversions(inversions, maxInversions)
    if sim is None:
        return None
    else:
        return 2.0*sim - 1.0

def similarityByInversions(inversions, maxInversions):
    """
    Similarity between sequences, given the inversions and max possible
    A similarity of 0 is the worst, while 1 is the best.
    @param inversions: Number of inversions
    @type inversions: int
    @param maxInversions: Maximum possible inversions
    @type maxInversions: int
    @return: Similarity, in [0, 1]
    @rtype: float
    """
    if maxInversions == 0:
        return None
    else:
        return 1.0 - float(inversions)/maxInversions

# Counts of Permutations with k Inversions
#------------------------------------------
def rawInversionCounts(n):
    """
    Get the count of the number of permutations with k inversions,
    as a vector of Inv(n,k) in the form [Inv(n,0), Inv(n,1), ..., Inv(n,k_max)]
    where n is the length of the sequence and k_max is the maximum inversions
    Note: This implementation uses the InversionCountsCache to boost speed
    @param n: Number of elements in the sequence
    @type n: int
    @return: List of inversion counts, where index k gives the # of permutations with k inversions
    @rtype: list of int
    """
    if n <= 0:
        return []
    elif n <= 1:
        return [1]
    else:
        value = InversionCountsCache.fetchCachedRawInversionCounts(n)
        if value is None:
            startingPoint = None
            cache = True
            cacheSize = InversionCountsCache.getCacheSize()
            if n >= cacheSize:
                maxCacheN = cacheSize-1
                startingCounts = InversionCountsCache.fetchCachedRawInversionCounts(maxCacheN)
                if startingCounts is not None:
                    startingPoint = (maxCacheN, startingCounts)
                    cache = False
            value = _directCalcRawInversionCounts(n, startingPoint, cache)
        return value

def _directCalcRawInversionCounts(n, startingPoint=None, cache=True):
    """
    Calculate the count of the number of permutations with k inversions,
    as a vector of Inv(n,k) in the form [Inv(n,0), Inv(n,1), ..., Inv(n,k_max)]
    where n is the length of the sequence and k_max is the maximum inversions.
    Note: This implementation can be bootstrapped using a startingPoint, to avoid
    calculating known inversions (as the algorithm works through iterative transforms)
    @param n: Number of elements in the sequence
    @type n: int
    @param startingPoint: Pair of (x, rawInversionCounts(x)) where x<n.  Used to bootstrap the calculation.
    @type startingPoint: tuple of (int, list of int)
    @param cache: If True, cache the calculated values.  Else, ignore the cache.
    @type cache: bool
    @return: List of inversion counts, where index k gives the # of permutations with k inversions
    @rtype: list of int
    """
    absoluteMax = maxInversions(n)+1
    if startingPoint is None or startingPoint[0] > n:
        startingN = 2
        inversionCounts = [1]+[0]*int(absoluteMax-1)
    else:
        startingN, inversionCounts = startingPoint
    for i in xrange(startingN,n+1):
        aMax = int(maxInversions(i)+1)
        inversionCounts[0:aMax] = (sum(inversionCounts[max(0,j-(i-1)):j+1]) for j in xrange(0,aMax))
        if cache:
            InversionCountsCache.cacheRawInversionCounts(i, inversionCounts[0:aMax])
    return inversionCounts


# Cache Management
#------------------------------------------
class InversionCountsCache(object):
    """ A cache for managing stored  inversion count calculations """
    # Optimization Variables
    # Note: Cache increases by 10x for each next 100 entries (200~ 200MB, 300~2GB)
    DEFAULT_CACHE_SIZE = 100
    EXACT_DISTRIBUTION_CACHE = [None]*DEFAULT_CACHE_SIZE

    @classmethod
    def getCacheSize(cls):
        """
        Get the cache size
        @return: Size of the cache
        @rtype: int
        """
        return len(cls.EXACT_DISTRIBUTION_CACHE)

    @classmethod
    def setCacheSize(cls, n=DEFAULT_CACHE_SIZE):
        """
        Set the cache size
        @param n: New size of the cache.  By default, resets to DEFAULT_CACHE_SIZE
        @type n: int
        """
        if n != cls.getCacheSize():
            if n > cls.getCacheSize():
                cls.EXACT_DISTRIBUTION_CACHE.extend([None]*(n-cls.getCacheSize()))
            else:
                del cls.EXACT_DISTRIBUTION_CACHE[n:]
        
    @classmethod
    def fetchCachedRawInversionCounts(cls, n):
        """
        Fetch a value from the cache by index n, if available.
        @param n: Index of the cache to read
        @type n: int
        @return: Cached value at index n, or None if out of bounds
        @rtype: list of int or None
        """
        if n < cls.getCacheSize() and n >= 0:
            value = cls.EXACT_DISTRIBUTION_CACHE[n]
            if value is not None:
                return list(value)
            else:
                return None
        else:
            return None

    @classmethod
    def cacheRawInversionCounts(cls, n, counts):
        """
        Cache a value from the cache at index n
        @param n: Index of the cache to write
        @type n: int
        @param counts: List of counts of permutations with k inversions
        @type counts: list of int
        """
        if n < cls.getCacheSize() and n >= 0:
            cls.EXACT_DISTRIBUTION_CACHE[n] = tuple(counts)

    @classmethod
    def clear(cls):
        """
        Clear all cached values.  For general use, this should be unnecessary.
        """
        cls.EXACT_DISTRIBUTION_CACHE[:] = (None for i in xrange(len(cls.EXACT_DISTRIBUTION_CACHE)))
