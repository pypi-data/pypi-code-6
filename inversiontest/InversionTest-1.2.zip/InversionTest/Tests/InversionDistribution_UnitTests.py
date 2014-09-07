import unittest
from InversionTest.InversionDistribution import (
    InversionCountsCache, rawInversionCounts, maxInversions,
    meanOfInversions, varianceOfInversions, correlationByInversions,
    similarityByInversions, _directCalcRawInversionCounts)
                                    
class InversionDistributionTests(unittest.TestCase):
    CACHE_SIZE = 50
    INVERSION_COUNTS_CACHE = InversionCountsCache

    def setUp(self):
        self.INVERSION_COUNTS_CACHE.setCacheSize(self.CACHE_SIZE)
        self.INVERSION_COUNTS_CACHE.clear()

    def populateCache(self):
        cacheSize = self.INVERSION_COUNTS_CACHE.getCacheSize()
        self.INVERSION_COUNTS_CACHE.cacheRawInversionCounts(0, [])
        self.INVERSION_COUNTS_CACHE.cacheRawInversionCounts(1, [1])
        x = rawInversionCounts(cacheSize)

    def testMaxInversions_Zero(self):
        n = 0
        expectedValue = 0
        value = maxInversions(n)
        self.assertEqual(value, expectedValue)

    def testMaxInversions_One(self):
        n = 1
        expectedValue = 0
        value = maxInversions(n)
        self.assertEqual(value, expectedValue)

    def testMaxInversions_Two(self):
        n = 2
        expectedValue = 1
        value = maxInversions(n)
        self.assertEqual(value, expectedValue)

    def testMaxInversions_Ten(self):
        n = 10
        expectedValue = 45
        value = maxInversions(n)
        self.assertEqual(value, expectedValue)


    def testMeanInversions_Zero(self):
        n = 0
        expectedValue = 0
        value = meanOfInversions(n)
        self.assertEqual(value, expectedValue)

    def testMeanInversions_One(self):
        n = 1
        expectedValue = 0
        value = meanOfInversions(n)
        self.assertEqual(value, expectedValue)

    def testMeanInversions_Two(self):
        n = 2
        expectedValue = 0.5
        value = meanOfInversions(n)
        self.assertEqual(value, expectedValue)

    def testMeanInversions_Ten(self):
        n = 10
        expectedValue = 22.5
        value = meanOfInversions(n)
        self.assertEqual(value, expectedValue)


    def testVarianceInversions_Zero(self):
        n = 0
        expectedValue = 0
        value = varianceOfInversions(n)
        self.assertEqual(value, expectedValue)

    def testVarianceInversions_One(self):
        n = 1
        expectedValue = 0
        value = varianceOfInversions(n)
        self.assertEqual(value, expectedValue)

    def testVarianceInversions_Two(self):
        n = 2
        expectedValue = 0.25
        value = varianceOfInversions(n)
        self.assertEqual(value, expectedValue)

    def testVarianceInversions_Ten(self):
        n = 10
        expectedValue = 31.25
        value = varianceOfInversions(n)
        self.assertEqual(value, expectedValue)

    def testCorrelationByInversions_Null(self):
        x = 0
        xMax = 0
        expectedValue = None
        value = correlationByInversions(x,xMax)
        self.assertTrue(value is expectedValue)

    def testCorrelationByInversions_Lowest(self):
        x = 0
        xMax = 20
        expectedValue = 1
        value = correlationByInversions(x,xMax)
        self.assertEqual(value, expectedValue)

    def testCorrelationByInversions_Middle(self):
        x = 10
        xMax = 20
        expectedValue = 0
        value = correlationByInversions(x,xMax)
        self.assertEqual(value, expectedValue)

    def testCorrelationByInversions_Highest(self):
        x = 20
        xMax = 20
        expectedValue = -1
        value = correlationByInversions(x,xMax)
        self.assertEqual(value, expectedValue)


    def testSimilarityByInversions_Null(self):
        x = 0
        xMax = 0
        expectedValue = None
        value = similarityByInversions(x,xMax)
        self.assertTrue(value is expectedValue)

    def testSimilarityByInversions_Lowest(self):
        x = 0
        xMax = 20
        expectedValue = 1
        value = similarityByInversions(x,xMax)
        self.assertEqual(value, expectedValue)

    def testSimilarityByInversions_Middle(self):
        x = 10
        xMax = 20
        expectedValue = 0.5
        value = similarityByInversions(x,xMax)
        self.assertEqual(value, expectedValue)

    def testSimilarityByInversions_Highest(self):
        x = 20
        xMax = 20
        expectedValue = 0
        value = similarityByInversions(x,xMax)
        self.assertEqual(value, expectedValue)
    
    def testGetCacheSize(self):
        expectedSize = self.CACHE_SIZE
        self.assertEqual(len(self.INVERSION_COUNTS_CACHE.EXACT_DISTRIBUTION_CACHE), expectedSize)

    def testSetCacheSize(self):
        newSize = 50
        self.INVERSION_COUNTS_CACHE.setCacheSize(newSize)
        self.assertEqual(self.INVERSION_COUNTS_CACHE.getCacheSize(), newSize)
        self.assertEqual(len(self.INVERSION_COUNTS_CACHE.EXACT_DISTRIBUTION_CACHE), newSize)

    def testSetCacheSize_Default(self): 
        newSize = 50
        originalSize = self.INVERSION_COUNTS_CACHE.DEFAULT_CACHE_SIZE
        self.INVERSION_COUNTS_CACHE.setCacheSize(newSize)
        self.assertEqual(self.INVERSION_COUNTS_CACHE.getCacheSize(), newSize)
        self.assertEqual(len(self.INVERSION_COUNTS_CACHE.EXACT_DISTRIBUTION_CACHE), newSize)
        self.INVERSION_COUNTS_CACHE.setCacheSize()
        self.assertEqual(self.INVERSION_COUNTS_CACHE.getCacheSize(), originalSize)
        self.assertEqual(len(self.INVERSION_COUNTS_CACHE.EXACT_DISTRIBUTION_CACHE), originalSize)

    def testFetchCachedRawInversionCounts_Empty(self):
        cacheSize = self.INVERSION_COUNTS_CACHE.getCacheSize()
        index = int(cacheSize/2.0)
        value = self.INVERSION_COUNTS_CACHE.fetchCachedRawInversionCounts(index)
        expectedValue = None
        self.assertTrue(value is expectedValue)

    def testFetchCachedRawInversionCounts_BelowMax(self):
        self.populateCache()
        index = -1
        value = self.INVERSION_COUNTS_CACHE.fetchCachedRawInversionCounts(index)
        expectedValue = None
        self.assertTrue(value is expectedValue)

    def testFetchCachedRawInversionCounts_AboveMax(self):
        self.populateCache()
        cacheSize = self.INVERSION_COUNTS_CACHE.getCacheSize()
        index = cacheSize
        value = self.INVERSION_COUNTS_CACHE.fetchCachedRawInversionCounts(index)
        expectedValue = None
        self.assertTrue(value is expectedValue)

    def testFetchCachedRawInversionCounts_Min(self):
        self.populateCache()
        index = 0
        value = self.INVERSION_COUNTS_CACHE.fetchCachedRawInversionCounts(index)
        expectedValue = []
        self.assertEqual(value, expectedValue)

    def testFetchCachedRawInversionCounts_Max(self):
        self.populateCache()
        cacheSize = self.INVERSION_COUNTS_CACHE.getCacheSize()
        index = cacheSize-1
        value = self.INVERSION_COUNTS_CACHE.fetchCachedRawInversionCounts(index)
        expectedValue = _directCalcRawInversionCounts(index)
        self.assertEqual(value, expectedValue)

    def testCacheRawInversionCounts_Min(self):
        index = 0
        value = [100]
        self.INVERSION_COUNTS_CACHE.cacheRawInversionCounts(index, value)
        fetchedVal = self.INVERSION_COUNTS_CACHE.fetchCachedRawInversionCounts(index)
        self.assertEqual(value, fetchedVal)

    def testCacheRawInversionCounts_Max(self):
        index = self.INVERSION_COUNTS_CACHE.getCacheSize()-1
        value = [200]
        self.INVERSION_COUNTS_CACHE.cacheRawInversionCounts(index, value)
        fetchedVal = self.INVERSION_COUNTS_CACHE.fetchCachedRawInversionCounts(index)
        self.assertEqual(value, fetchedVal)

            
if __name__ == "__main__":
    unittest.main()
