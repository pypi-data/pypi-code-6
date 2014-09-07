import unittest
from InversionTest.StatisticalTests import (
    binomialTest, signTest, wilcoxonSignedRankTest,
    permutationMeanTest, permutationRankTest,
    GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS)
from InversionTest.InversionAnalysis import (
    MissingElementError, InvalidGradedPosetError, 
    GradedPosetSequence, filterElements, getMedianValue, getValueIndex,
    makeFlatIndexSequence, makeIndexSequence, inversionCountMax,
    inversionCountMean, inversionCountVariance, medianSequence,
    mergeSortInversionCount, inversionCount, inversionSimilarity,
    inversionCountCDF, inversionSignTest, inversionWilcoxonTest,
    inversionPermutationMeanTest, inversionPermutationRankTest,
    CDF_TYPES, EXACT_CDF, NORMAL_CDF, ADAPTIVE_CDF, SIMILARITY_METRIC)

class InversionAnalysis_FunctionsTest(unittest.case.TestCase):

    # Descriptive Measures
    def testInversionCountMax_Empty(self):
        n = inversionCountMax([])
        self.assertEqual(n, 0)
        nWithCensored = inversionCountMax([[1,2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 0)

    def testInversionCountMax_Single(self):
        n = inversionCountMax([1])
        self.assertEqual(n, 0)
        nWithCensored = inversionCountMax([[1], [2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 3)
        nWithCensored = inversionCountMax([[5], [1,2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 4)

    def testInversionCountMax_Two(self):
        n = inversionCountMax([1,2])
        self.assertEqual(n, 1)
        nWithCensored = inversionCountMax([[1,2], [3]], isGraded=True)
        self.assertEqual(nWithCensored, 2)
        nWithCensored = inversionCountMax([[3,4], [1,2]], isGraded=True)
        self.assertEqual(nWithCensored, 4)

    def testInversionCountMax_WithComparison(self):
        self.assertEqual(6, inversionCountMax(range(1,5), range(1,5)))
        self.assertEqual(6, inversionCountMax(range(1,5), range(1,5), isGraded=False))
        self.assertEqual(6, inversionCountMax([[1],[2],[3],[4]], [[1],[2],[3],[4]], isGraded=True))
        self.assertEqual(6, inversionCountMax([1,2,3,[4]], [[1],[2],[3],[4]], isGraded=True))
        self.assertEqual(6, inversionCountMax([[1],[2],[3],[4]], [1,2,3,[4]], isGraded=True))
        self.assertEqual(6, inversionCountMax([[1],[2],[3],[4]], [[4],[3],[2],[1]], isGraded=True))
        self.assertEqual(3, inversionCountMax([[1],[2],[3],[4]], [[1],[2],[3]], isGraded=True))
        # Note: Actual inversion count will fail in this case (as 5 has no index in the other)
        self.assertEqual(3, inversionCountMax(range(1,4), range(1,5)))

    def testInversionCountMax_WithComparison_Posets(self):
        self.assertEqual(6, inversionCountMax(GradedPosetSequence(range(1,5)), GradedPosetSequence(range(1,5))))
        self.assertEqual(6, inversionCountMax(GradedPosetSequence(range(1,5)), GradedPosetSequence(range(1,5)), isGraded=False))
        self.assertEqual(6, inversionCountMax(GradedPosetSequence([[1],[2],[3],[4]], isGraded=True),
                                              GradedPosetSequence([[1],[2],[3],[4]], isGraded=True), isGraded=True))
        self.assertEqual(6, inversionCountMax(GradedPosetSequence([1,2,3,[4]], isGraded=True),
                                              GradedPosetSequence([[1],[2],[3],[4]], isGraded=True), isGraded=True))
        self.assertEqual(6, inversionCountMax(GradedPosetSequence([[1],[2],[3],[4]], isGraded=True),
                                              GradedPosetSequence([1,2,3,[4]], isGraded=True), isGraded=True))
        self.assertEqual(6, inversionCountMax(GradedPosetSequence([[1],[2],[3],[4]], isGraded=True),
                                              GradedPosetSequence([[4],[3],[2],[1]], isGraded=True), isGraded=True))
        self.assertEqual(3, inversionCountMax(GradedPosetSequence([[1],[2],[3],[4]], isGraded=True),
                                              GradedPosetSequence([[1],[2],[3]], isGraded=True), isGraded=True))
        # Note: Actual inversion count will fail in this case (as 5 has no index in the other)
        self.assertEqual(3, inversionCountMax(GradedPosetSequence(range(1,4)), GradedPosetSequence(range(1,5))))

    def testInversionCountMean_Empty(self):
        n = inversionCountMean([])
        self.assertEqual(n, 0)
        nWithCensored = inversionCountMean([[1,2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 0)

    def testInversionCountMean_Single(self):
        n = inversionCountMean([1])
        self.assertEqual(n, 0)
        nWithCensored = inversionCountMean([[1], [2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 1.5)
        nWithCensored = inversionCountMean([[5], [1,2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 2)
        nWithCensored2 = inversionCountMean([5, [1,2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 2)

    def testInversionCountMean_Two(self):
        n = inversionCountMean([1,2])
        self.assertEqual(n, 0.5)
        nWithCensored = inversionCountMean([[1,2], [3]], isGraded=True)
        self.assertEqual(nWithCensored, 1)
        nWithCensored = inversionCountMean([[3,4], [1,2]], isGraded=True)
        self.assertEqual(nWithCensored, 2)

    def testInversionCountMean_WithComparison(self):
        self.assertEqual(3, inversionCountMean(range(1,5), range(1,5)))
        self.assertEqual(3, inversionCountMean(range(1,5), range(1,5), isGraded=False))
        self.assertEqual(3, inversionCountMean([[1],[2],[3],[4]], [[1],[2],[3],[4]], isGraded=True))
        self.assertEqual(3, inversionCountMean([[1],[2],[3],[4]], [[4],[3],[2],[1]], isGraded=True))
        self.assertEqual(1.5, inversionCountMean([[1],[2],[3],[4]], [[1],[2],[3]], isGraded=True))
        # Note: Actual inversion count will fail in this case (as 5 has no index in the other)
        self.assertEqual(1.5, inversionCountMean(range(1,4), range(1,5)))

    def testInversionCountVariance_Empty(self):
        n = inversionCountVariance([])
        self.assertEqual(n, 0)
        nWithCensored = inversionCountVariance([[1,2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 0)

    def testInversionCountVariance_Single(self):
        n = inversionCountVariance([1])
        self.assertEqual(n, 0)
        nWithCensored = inversionCountVariance([[1], [2,3,4]], isGraded=True)
        self.assertEqual(nWithCensored, 1.25)
        nWithCensored = inversionCountVariance([[5], [1,2,3,4]], isGraded=True)
        self.assertAlmostEqual(nWithCensored, 2.0)

    def testInversionCountVariance_Two(self):
        n = inversionCountVariance([1,2])
        self.assertEqual(n, 0.25)
        nWithCensored = inversionCountVariance([[1,2], [3]], isGraded=True)
        self.assertAlmostEqual(nWithCensored, 2.0/3.0)
        nWithCensored = inversionCountVariance([[3,4], [1,2]], isGraded=True)
        self.assertAlmostEqual(nWithCensored, 5.0/3.0)

    def testInversionCountVariance_WithComparison(self):
        self.assertAlmostEqual(13.0/6.0, inversionCountVariance(range(1,5), range(1,5)))
        self.assertAlmostEqual(13.0/6.0, inversionCountVariance(range(1,5), range(1,5), isGraded=False))
        self.assertAlmostEqual(13.0/6.0, inversionCountVariance([[1],[2],[3],[4]], [[1],[2],[3],[4]], isGraded=True))
        self.assertAlmostEqual(13.0/6.0, inversionCountVariance([[1],[2],[3],[4]], [[4],[3],[2],[1]], isGraded=True))
        self.assertAlmostEqual(11.0/12.0, inversionCountVariance([[1],[2],[3],[4]], [[1],[2],[3]], isGraded=True))
        self.assertAlmostEqual(11.0/12.0, inversionCountVariance([[1],2,[3],[4]], [1,[2],[3]], isGraded=True))
        # Note: Actual inversion count will fail in this case (as 5 has no index in the other)
        self.assertAlmostEqual(11.0/12.0, inversionCountVariance(range(1,4), range(1,5)))

    def testMedianSequence_Empty(self):
        self.assertEqual([], medianSequence([]))
        self.assertEqual([], medianSequence([], isGraded=True))
        self.assertEqual([], medianSequence([], hashableElements=False))
        self.assertEqual([], medianSequence([], isGraded=True, hashableElements=False))

    def testMedianSequence_Odd(self):
        permutations = [range(5), range(5), range(4,-1,-1)]
        expected = [[i] for i in range(5)]
        self.assertEqual(expected, medianSequence(permutations))
        self.assertEqual(expected, medianSequence(permutations, hashableElements=False ))

    def testMedianSequence_Even(self):
        permutations = [range(5), range(5), range(4,-1,-1), range(4,-1,-1)]
        expected = [range(5)]
        self.assertEqual(expected, medianSequence(permutations))
        self.assertEqual(expected, medianSequence(permutations, hashableElements=False))

    def testMedianSequence_Nested_Odd(self):
        permutations = [range(5), range(5), range(4,-1,-1)]
        nestedPermutations = [[[x] for x in p] for p in permutations]
        expected = [[i] for i in range(5)]
        self.assertEqual(expected, medianSequence(permutations, isGraded=True))
        self.assertEqual(expected, medianSequence(permutations, isGraded=True, hashableElements=False))
        self.assertEqual(expected, medianSequence(nestedPermutations, isGraded=True))
        self.assertEqual(expected, medianSequence(nestedPermutations, isGraded=True, hashableElements=False))

    def testMedianSequence_Nested_Even(self):
        permutations = [range(5), range(5), range(4,-1,-1), range(4,-1,-1)]
        nestedPermutations = [[[x] for x in p] for p in permutations]
        expected = [range(5)]
        self.assertEqual(expected, medianSequence(permutations, isGraded=True))
        self.assertEqual(expected, medianSequence(permutations, isGraded=True, hashableElements=False))
        self.assertEqual(expected, medianSequence(nestedPermutations, isGraded=True))
        self.assertEqual(expected, medianSequence(nestedPermutations, isGraded=True, hashableElements=False))
        
    # Inversion Measures
    def testMergeSortInversionCount_Empty(self):
        self.assertEqual(mergeSortInversionCount([]), (0,[]))

    def testMergeSortInversionCount_Single(self):
        self.assertEqual(mergeSortInversionCount([4]), (0,[4])) 

    def testMergeSortInversionCount_Two(self):
        self.assertEqual(mergeSortInversionCount([1,2]), (0,[1,2])) 
        self.assertEqual(mergeSortInversionCount([2,1]), (1,[1,2])) 
        self.assertEqual(mergeSortInversionCount([10,-1]), (1,[-1,10]))

    def testMergeSortInversionCount_Three(self):
        self.assertEqual(mergeSortInversionCount([1,2,3]), (0,[1,2,3]))
        self.assertEqual(mergeSortInversionCount([2,1,3]), (1,[1,2,3]))
        self.assertEqual(mergeSortInversionCount([1,3,2]), (1,[1,2,3]))
        self.assertEqual(mergeSortInversionCount([2,3,1]), (2,[1,2,3]))
        self.assertEqual(mergeSortInversionCount([3,2,1]), (3,[1,2,3]))

    def testInversionCount_NoCensored(self):
        refList = [1,2,3,4]
        testList = [4,2,1,3]
        count = 4
        maxInversions = 6
        n = inversionCount(testList, refList)
        self.assertEqual(n, count)

    def testInversionCount_NoCensoredNestedRefs(self):
        refList = [1,2,3,4]
        nestedRefList = [[1],[2],[3],[4]]
        partiallyNestedRefList = [1,[2],[3],4]
        testList = [[4],[2],[1],[3]]
        testList2 = [4,[2],[1],3]
        testList3 = [4,2,1,3]
        count = 4
        maxInversions = 6
        self.assertEqual(count, inversionCount(testList, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, partiallyNestedRefList, isGraded=True))

    def testInversionCount_NoCensoredNestedRefs_PosetRefs(self):
        refList = GradedPosetSequence([1,2,3,4])
        nestedRefList = GradedPosetSequence([[1],[2],[3],[4]], isGraded=True)
        partiallyNestedRefList = GradedPosetSequence([1,[2],[3],4], isGraded=True)
        testList = [[4],[2],[1],[3]]
        testList2 = [4,[2],[1],3]
        testList3 = [4,2,1,3]
        count = 4
        maxInversions = 6
        self.assertEqual(count, inversionCount(testList, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, partiallyNestedRefList, isGraded=True))

    def testInversionCount_NoCensoredNestedRefs_PosetComps(self):
        refList = [1,2,3,4]
        nestedRefList = [[1],[2],[3],[4]]
        partiallyNestedRefList = [1,[2],[3],4]
        testList = GradedPosetSequence([[4],[2],[1],[3]], isGraded=True)
        testList2 = GradedPosetSequence([4,[2],[1],3], isGraded=True)
        testList3 = GradedPosetSequence([4,2,1,3])
        count = 4
        maxInversions = 6
        self.assertEqual(count, inversionCount(testList, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, partiallyNestedRefList, isGraded=True))

    def testInversionCount_NoCensoredNestedRefs_PosetBoth(self):
        refList = GradedPosetSequence([1,2,3,4])
        nestedRefList = GradedPosetSequence([[1],[2],[3],[4]], isGraded=True)
        partiallyNestedRefList = GradedPosetSequence([1,[2],[3],4], isGraded=True)
        testList = GradedPosetSequence([[4],[2],[1],[3]], isGraded=True)
        testList2 = GradedPosetSequence([4,[2],[1],3], isGraded=True)
        testList3 = GradedPosetSequence([4,2,1,3])
        count = 4
        maxInversions = 6
        self.assertEqual(count, inversionCount(testList, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, refList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, nestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList2, partiallyNestedRefList, isGraded=True))
        self.assertEqual(count, inversionCount(testList3, partiallyNestedRefList, isGraded=True))

    def testInversionCount_CensoredData(self):
        refList = [[1],[2],[3],[4],[5]]
        testList = [[4],[1],[5],[3,2]]
        count = 5
        maxInversions = 9
        n = inversionCount(testList, refList, isGraded=True)
        self.assertEqual(n, count)

    def testInversionCount_CensoredRefs(self):
        refList = [[1],[2],[3],[4]]
        testList = [[6],[5],[4],[1],[5,6]]
        count = 5
        maxInversions = 5
        self.assertRaises(MissingElementError, inversionCount, testList, refList, isGraded=True)

    def testInversionCount_CensoredBoth(self):
        refList = [[1],[2],[3],[4],[5,6]]
        testList = [[6],[5],[4],[1],[3,2]]
        count = 11
        maxInversions = 13
        n = inversionCount(testList, refList, isGraded=True)
        self.assertEqual(n, count)

    def testInversionCount_CensoredBoth_OneExcluded(self):
        refList = [[1],[3],[4],[5,6]]
        testList = [[6],[5],[4],[1],[3,2]]
        excludedElements = [2]
        count = 8
        maxInversions = 9
        n = inversionCount(testList, refList, isGraded=True)
        self.assertEqual(n, count)

    def testInversionCount_CensoredBoth_TwoExcluded(self):
        refList = [[1],[3],[5,6]]
        testList = [[6],[5],[4],[1],[3,2]]
        excludedElements = [2,4]
        count = 4
        maxInversions = 5
        n = inversionCount(testList, refList, isGraded=True)
        self.assertEqual(n, count)

    def testInversionCount_TranslatingExample(self):
        refList = [['S_05'], ['S_09'], ['S_04','S_01'], ['S_06'], ['S_08'], ['S_03'], ['S_00'], ['S_02']]
        testList = [['S_05'], ['S_09'], ['S_04','S_01'], ['S_06'], ['S_08'], ['S_03'], ['S_00'], ['S_02']]
        n = inversionCount(testList, refList, isGraded=True)
        nMax = inversionCountMax(testList, refList, isGraded=True)
        self.assertEqual(n, 0)
        self.assertEqual(nMax, 35)

    def testInversionCount_TranslatingExampleWithExclusions(self):
        refList = [['S_09'], ['S_04','S_01'], ['S_06'], ['S_08'], ['S_03'], ['S_02']]
        testList = [['S_05'], ['S_09'], ['S_04','S_01'], ['S_06'], ['S_08'], ['S_03'], ['S_00'], ['S_02']]
        excludedElements = ['S_05','S_00']
        n = inversionCount(testList, refList, isGraded=True)
        nMax = inversionCountMax(testList, refList, isGraded=True)
        self.assertEqual(n, 0)
        self.assertEqual(nMax, 20)
        
    def testInversionCount_AllTies(self):
        refList = [[1],[2],[3],[4]]
        refList2 = [1,2,3,4]
        testList = [[4,2,1,3]]
        self.assertEqual(inversionCount(testList, refList, isGraded=True), 0)
        self.assertEqual(inversionCountMax(testList, refList, isGraded=True), 0)
        self.assertEqual(inversionCount(testList, refList2, isGraded=True), 0)
        self.assertEqual(inversionCountMax(testList, refList2, isGraded=True), 0)

    def testInversionSimilarity_Single(self):
        self.assertEqual(0.0, inversionSimilarity(range(9,-1,-1)))
        self.assertEqual(1.0, inversionSimilarity(range(10)))

    def testInversionSimilarity_SingleNested(self):
        self.assertEqual(0.0, inversionSimilarity([[i] for i in range(9,-1,-1)], isGraded=True))
        self.assertEqual(1.0, inversionSimilarity([[i] for i in range(10)], isGraded=True))

    def testInversionSimilarity_Compare(self):
        seq = range(9,-1,-1)
        comp1 = range(9,-1,-1)
        comp2 = range(10)
        self.assertEqual(1.0, inversionSimilarity(seq, comp1))
        self.assertEqual(0.0, inversionSimilarity(seq, comp2))
        
    def testInversionSimilarity_CompareNested(self):
        seq = [[x] for x in range(9,-1,-1)]
        comp1 = [[i] for i in range(9,-1,-1)]
        comp2 = [[i] for i in range(10)]
        self.assertEqual(1.0, inversionSimilarity(seq, [[i] for i in range(9,-1,-1)], isGraded=True))
        self.assertEqual(0.0, inversionSimilarity(seq, [[i] for i in range(10)], isGraded=True))

    # Utility Functions
    def testGetMedianValue(self):
        self.assertRaises(IndexError, getMedianValue, [])
        self.assertEqual(2, getMedianValue(range(5)))
        self.assertEqual(1.5, getMedianValue(range(4)))
        
    def testGetValueIndex(self):
        refList = [1,2,3,4]
        self.assertEqual(getValueIndex(3, refList, isGraded=False), 2)
        self.assertRaises(MissingElementError, getValueIndex, 10, refList)

    def testGetValueIndex_Nested(self):
        refList = [[1],[2,3],[4]]
        self.assertEqual(getValueIndex(2, refList, isGraded=True), 1)
        self.assertEqual(getValueIndex(3, refList, isGraded=True), 1)
        self.assertEqual(getValueIndex(4, refList, isGraded=True), 2)

    def testGetValueIndex_NestedWithCensored(self):
        refList = [[1],[2,3],[4], [5,6]]
        self.assertEqual(getValueIndex(2, refList, isGraded=True), 1)
        self.assertEqual(getValueIndex(3, refList, isGraded=True), 1)
        self.assertEqual(getValueIndex(4, refList, isGraded=True), 2)
        self.assertEqual(getValueIndex(5, refList, isGraded=True), 3)
        self.assertEqual(getValueIndex(6, refList, isGraded=True), 3)

    def testMakeIndexSequence_BothFlat(self):
        sequence = ['A', 'B', 'G', 'C', 'D', 'E', 'F']
        referenceSequence = list('ABCDEFG')
        result = [0,1,6,2,3,4,5]
        self.assertEqual(result, makeIndexSequence(sequence, referenceSequence))

    def testMakeIndexSequence_NestedSequence(self):
        sequence = [['A'], ['B','G'], ['C'], ['D'], ['E'], ['F']]
        referenceSequence = list('ABCDEFG')
        result = [[0],[1,6],[2],[3],[4],[5]]
        self.assertEqual(result, makeIndexSequence(sequence, referenceSequence, isSeqNested=True))

    def testMakeIndexSequence_NestedReference(self):
        sequence = ['A', 'B', 'G', 'C', 'D', 'E', 'F']
        referenceSequence = [[s] for s in 'ABCDEFG']
        result = [0,1,6,2,3,4,5]
        self.assertEqual(result, makeIndexSequence(sequence, referenceSequence, isRefNested=True))

    def testMakeIndexSequence_BothNested(self):
        sequence = [['A'], ['B','G'], ['C'], ['D'], ['E'], ['F']]
        referenceSequence = [[s] for s in 'ABCDEFG']
        result = [[0],[1,6],[2],[3],[4],[5]]
        self.assertEqual(result, makeIndexSequence(sequence, referenceSequence, isRefNested=True, isSeqNested=True))

    def testMakeFlatIndexSequence_BothFlat(self):
        sequence = ['A', 'B', 'G', 'C', 'D', 'E', 'F']
        referenceSequence = list('ABCDEFG')
        result = [0,1,6,2,3,4,5]
        self.assertEqual(result, makeFlatIndexSequence(sequence, referenceSequence))

    def testMakeFlatIndexSequence_NestedSequence(self):
        sequence = [['A'], ['B','G'], ['C'], ['D'], ['E'], ['F']]
        referenceSequence = list('ABCDEFG')
        result = [0,1,6,2,3,4,5]
        self.assertEqual(result, makeFlatIndexSequence(sequence, referenceSequence, isSeqNested=True))

    def testMakeFlatIndexSequence_NestedReference(self):
        sequence = ['A', 'B', 'G', 'C', 'D', 'E', 'F']
        referenceSequence = [[s] for s in 'ABCDEFG']
        result = [0,1,6,2,3,4,5]
        self.assertEqual(result, makeFlatIndexSequence(sequence, referenceSequence, isRefNested=True))

    def testMakeFlatIndexSequence_BothNested(self):
        sequence = [['A'], ['B','G'], ['C'], ['D'], ['E'], ['F']]
        referenceSequence = [[s] for s in 'ABCDEFG']
        result = [0,1,6,2,3,4,5]
        self.assertEqual(result, makeFlatIndexSequence(sequence, referenceSequence, isRefNested=True, isSeqNested=True))

    def testFilterElements_NestedSequenceNoExclusions(self):
        nestedSeq = [[1],[2],[3],[4,5,6]]
        newNestedSeq = filterElements(nestedSeq, [], True)
        self.assertEqual(nestedSeq, newNestedSeq)
        newNestedSeq = filterElements(nestedSeq, [], True)
        self.assertEqual(nestedSeq, newNestedSeq)

    def testFilterElements_NestedSequenceOneExclusion(self):
        nestedSeq = [[1],[2],[3],[4,5,6]]
        newNestedSeq = filterElements(nestedSeq, [2], True)
        self.assertEqual(newNestedSeq, [[1],[3],[4,5,6]])

    def testFilterElementsFromNestedSequence_TwoExclusions(self):
        nestedSeq = [[1],[2],[3],[4,5,6]]
        newNestedSeq = filterElements(nestedSeq, [2,5], True)
        self.assertEqual(newNestedSeq, [[1],[3],[4,6]])
    
    # Probability and Statistics
    def testInversionCountCDF(self):
        refList = [1,2,3,4]
        testList = [4,2,1,3]
        count = 4
        maxInversions = 6
        pActual = 20.0/24.0
        probability = inversionCountCDF(testList, refList)
        self.assertEqual(pActual, probability)

    def testInversionCountCDF_Exact(self):
        refList = [1,2,3,4]
        testList = [4,2,1,3]
        count = 4
        maxInversions = 6
        pActual = 20.0/24.0
        self.assertEqual(pActual, inversionCountCDF(testList, refList, cdfType=EXACT_CDF))
        self.assertEqual(pActual, inversionCountCDF(testList, refList, cdfType=ADAPTIVE_CDF))

    def testInversionCountCDF_NormalApproximation(self):
        refList = range(10)
        testList = [9]+range(9)
        count = 9
        maxInversions = 45
        pActual = 0.008333
        pApprox = 0.007869
        estimate = inversionCountCDF(testList, refList, cdfType=NORMAL_CDF)
        self.assertAlmostEqual(pApprox, estimate, 4)
        # Error should be less than 10% even at length of 10
        self.assertTrue(abs(pActual-estimate)/estimate < 0.1)

    def testInversionCountCDF_Large(self):
        refList = [999] + range(999)
        testList = sorted(range(1000), reverse=True)
        self.assertEqual(1.0, inversionCountCDF(testList, refList))
        self.assertEqual(0.0, inversionCountCDF(refList, refList))

    def testInversionCountCDF_LargeNormalApproximation(self):
        refList = range(1000)
        testList = sorted(range(1000), reverse=True)
        self.assertEqual(1.0, inversionCountCDF(testList, refList, cdfType=NORMAL_CDF))
        self.assertEqual(0.0, inversionCountCDF(refList, refList, cdfType=NORMAL_CDF))
        
    def testInversionSignTest(self):
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        signs1 = [inversionCount(x) < inversionCountMean(x) for x in permutations1 if
                  inversionCount(x) != inversionCountMean(x)]
        signs2 = [inversionCount(x) < inversionCountMean(x) for x in permutations2 if
                  inversionCount(x) != inversionCountMean(x)]
        #GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        # Binomials
        self.assertEqual(inversionSignTest(permutations1, seq=refList),
                         binomialTest(sum(signs1), len(signs1), 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList),
                         binomialTest(sum(signs2), len(signs2), 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations1, seq=refList, alternative=LESS_THAN_HYPOTHESIS),
                         binomialTest(sum(signs1), len(signs1), 0.5, LESS_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, alternative=LESS_THAN_HYPOTHESIS),
                         binomialTest(sum(signs2), len(signs2), 0.5, LESS_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations1, seq=refList, alternative=TWO_SIDED_HYPOTHESIS),
                         binomialTest(sum(signs1), len(signs1), 0.5, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, alternative=TWO_SIDED_HYPOTHESIS),
                         binomialTest(sum(signs2), len(signs2), 0.5, TWO_SIDED_HYPOTHESIS))
        # Sign Test Comparison
        vals1 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations1]
        vals2 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations2]
        self.assertEqual(inversionSignTest(permutations1, seq=refList),
                         signTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList),
                         signTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertEqual(inversionSignTest(nestedPerm1, seq=nestedRef, isGraded=True),
                         signTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(nestedPerm2, seq=nestedRef, isGraded=True),
                         signTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))

    def testInversionSignTest_TwoSample(self):
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        signs1 = [inversionCount(x) < inversionCountMean(x) for x in permutations1 if
                  inversionCount(x) != inversionCountMean(x)]
        signs2 = [inversionCount(x) < inversionCountMean(x) for x in permutations2 if
                  inversionCount(x) != inversionCountMean(x)]
        #GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        # Sign Test Comparison
        vals1 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations1]
        vals2 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations2]
        self.assertEqual(inversionSignTest(permutations1, permutations2, seq=refList),
                         signTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, permutations1, seq=refList),
                         signTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS))
        # No Reference sequence
        self.assertEqual(inversionSignTest(permutations1, permutations2),
                         signTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, permutations1),
                         signTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS))
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertEqual(inversionSignTest(nestedPerm1, nestedPerm2, seq=nestedRef, isGraded=True),
                         signTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(nestedPerm2, nestedPerm1, seq=nestedRef, isGraded=True),
                         signTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS))

    def testInversionSignTest_CDF(self):
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        signs1 = [inversionCount(x) < inversionCountMean(x) for x in permutations1 if
                  inversionCount(x) != inversionCountMean(x)]
        signs2 = [inversionCount(x) < inversionCountMean(x) for x in permutations2 if
                  inversionCount(x) != inversionCountMean(x)]
        # Binomials
        self.assertEqual(inversionSignTest(permutations1, seq=refList, measure=ADAPTIVE_CDF),
                         binomialTest(sum(signs1), len(signs1), 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, measure=ADAPTIVE_CDF),
                         binomialTest(sum(signs2), len(signs2), 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations1, seq=refList, alternative=LESS_THAN_HYPOTHESIS, measure=ADAPTIVE_CDF),
                         binomialTest(sum(signs1), len(signs1), 0.5, LESS_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, alternative=LESS_THAN_HYPOTHESIS, measure=ADAPTIVE_CDF),
                         binomialTest(sum(signs2), len(signs2), 0.5, LESS_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations1, seq=refList, alternative=TWO_SIDED_HYPOTHESIS, measure=ADAPTIVE_CDF),
                         binomialTest(sum(signs1), len(signs1), 0.5, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, alternative=TWO_SIDED_HYPOTHESIS, measure=ADAPTIVE_CDF),
                         binomialTest(sum(signs2), len(signs2), 0.5, TWO_SIDED_HYPOTHESIS))
        # Sign Test Comparison (Similarity should be same as CDF for this)
        vals1 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations1]
        vals2 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations2]
        self.assertEqual(inversionSignTest(permutations1, seq=refList, measure=ADAPTIVE_CDF),
                         signTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, measure=ADAPTIVE_CDF),
                         signTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))

    def testInversionSignTest_MuDifference(self):
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        vals1 = [1.0-float(inversionCount(x))/inversionCountMax(x)  for x in permutations1]
        vals2 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations2]
        #GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        self.assertEqual(inversionSignTest(permutations1, seq=refList, mu=0.7),
                         signTest(vals1, mu=0.7, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, mu=0.7),
                         signTest(vals2, mu=0.7, alternative=GREATER_THAN_HYPOTHESIS))


    def testInversionSignTest_MuDifference_CDF(self):
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        vals1 = [1.0-inversionCountCDF(x) for x in permutations1]
        vals2 = [1.0-inversionCountCDF(x) for x in permutations2]
        self.assertEqual(inversionSignTest(permutations1, seq=refList, mu=0.7, measure=ADAPTIVE_CDF),
                         signTest(vals1, mu=0.7, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, mu=0.7, measure=ADAPTIVE_CDF),
                         signTest(vals2, mu=0.7, alternative=GREATER_THAN_HYPOTHESIS))
        # Similarity will not always be the same as CDF for this
        simVals1 = [1.0-float(inversionCount(x))/inversionCountMax(x)  for x in permutations1]
        simVals2 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations2]
        self.assertNotEqual(inversionSignTest(permutations1, seq=refList, mu=0.7, measure=ADAPTIVE_CDF),
                            signTest(simVals1, mu=0.7, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionSignTest(permutations2, seq=refList, mu=0.7, measure=ADAPTIVE_CDF),
                         signTest(simVals2, mu=0.7, alternative=GREATER_THAN_HYPOTHESIS))        

    def testInversionWilcoxonTest(self):
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        # Wilcoxon Tests
        vals1 = [1.0-inversionCountCDF(x) for x in permutations1]
        vals2 = [1.0-inversionCountCDF(x) for x in permutations2]
        self.assertEqual(inversionWilcoxonTest(permutations1, seq=refList),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionWilcoxonTest(permutations2, seq=refList),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionWilcoxonTest(permutations1, seq=refList, alternative=LESS_THAN_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=LESS_THAN_HYPOTHESIS))
        self.assertEqual(inversionWilcoxonTest(permutations2, seq=refList, alternative=LESS_THAN_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=LESS_THAN_HYPOTHESIS))
        self.assertEqual(inversionWilcoxonTest(permutations1, seq=refList, alternative=TWO_SIDED_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=TWO_SIDED_HYPOTHESIS))
        self.assertEqual(inversionWilcoxonTest(permutations2, seq=refList, alternative=TWO_SIDED_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=TWO_SIDED_HYPOTHESIS)) 

        # No Reference Seq
        self.assertEqual(inversionWilcoxonTest(permutations1),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionWilcoxonTest(permutations2),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertEqual(inversionWilcoxonTest(nestedPerm1, seq=nestedRef, isGraded=True),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(inversionWilcoxonTest(nestedPerm2, seq=nestedRef, isGraded=True),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))


    def testInversionPermutationMeanTest(self):
        places = 2
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        #GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        # Original Test Comparison
        vals1 = [1.0-inversionCountCDF(x) for x in permutations1]
        vals2 = [1.0-inversionCountCDF(x) for x in permutations2]
        
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations1, permutations2, seq=refList),
                               permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations2, permutations1, seq=refList),
                         permutationMeanTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        self.assertAlmostEqual(inversionPermutationMeanTest(permutations1, permutations2, seq=refList,
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationMeanTest(vals1, vals2, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations2, permutations1, seq=refList,
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationMeanTest(vals2, vals1, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations1, permutations2, seq=refList,
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationMeanTest(vals1, vals2, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations2, permutations1, seq=refList,
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationMeanTest(vals2, vals1, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations1, permutations2, seq=refList,
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationMeanTest(vals1, vals2, TWO_SIDED_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations2, permutations1, seq=refList,
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationMeanTest(vals2, vals1, TWO_SIDED_HYPOTHESIS), places)
        
        # No Reference sequence
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations1, permutations2),
                         permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations2, permutations1),
                         permutationMeanTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertAlmostEqual(inversionPermutationMeanTest(nestedPerm1, nestedPerm2, seq=nestedRef, isGraded=True),
                         permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationMeanTest(nestedPerm2, nestedPerm1, seq=nestedRef, isGraded=True),
                         permutationMeanTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        # Params Tests
        self.assertAlmostEqual(inversionPermutationMeanTest(permutations1, permutations2, seq=refList,
                                                            isGraded=False, hashableElements=True,
                                                            measure=ADAPTIVE_CDF, pValue=0.8,
                                                            iterations=10000, useStoppingRule=False,
                                                            maxExactN=10),
                               permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS,
                                                   pValue=0.8, iterations=10000, useStoppingRule=False,
                                                   maxExactN=10), places)
        
    def testInversionPermutationRankTest(self):
        places = 2 
        refList = range(10)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        #GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        # Original Test Comparison
        vals1 = [1.0-inversionCountCDF(x) for x in permutations1]
        vals2 = [1.0-inversionCountCDF(x) for x in permutations2]
        
        self.assertAlmostEqual(inversionPermutationRankTest(permutations1, permutations2, seq=refList),
                               permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(permutations2, permutations1, seq=refList),
                         permutationRankTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        self.assertAlmostEqual(inversionPermutationRankTest(permutations1, permutations2, seq=refList,
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationRankTest(vals1, vals2, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(permutations2, permutations1, seq=refList,
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationRankTest(vals2, vals1, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(permutations1, permutations2, seq=refList,
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationRankTest(vals1, vals2, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(permutations2, permutations1, seq=refList,
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationRankTest(vals2, vals1, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(permutations1, permutations2, seq=refList,
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationRankTest(vals1, vals2, TWO_SIDED_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(permutations2, permutations1, seq=refList,
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationRankTest(vals2, vals1, TWO_SIDED_HYPOTHESIS), places)
        
        # No Reference sequence
        self.assertAlmostEqual(inversionPermutationRankTest(permutations1, permutations2),
                         permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(permutations2, permutations1),
                         permutationRankTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertAlmostEqual(inversionPermutationRankTest(nestedPerm1, nestedPerm2, seq=nestedRef, isGraded=True),
                         permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(inversionPermutationRankTest(nestedPerm2, nestedPerm1, seq=nestedRef, isGraded=True),
                         permutationRankTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        # Params Tests
        self.assertAlmostEqual(inversionPermutationRankTest(permutations1, permutations2, seq=refList,
                                                            isGraded=False, hashableElements=True,
                                                            measure=ADAPTIVE_CDF, pValue=0.8,
                                                            iterations=10000, useStoppingRule=False,
                                                            maxExactN=10),
                               permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS,
                                                   pValue=0.8, iterations=10000, useStoppingRule=False,
                                                   maxExactN=10), places)

class GradedPosetSequenceTest(unittest.case.TestCase):

    def setUp(self):
        self.sequence = range(10)
        self.nestedSeq = [[x] for x in xrange(8)] + [[8,9]]
        self.reversedSeq = list(reversed(self.sequence))
        self.reversedNestedSeq = list(reversed(self.nestedSeq))
        self.refPoset = GradedPosetSequence(self.sequence)
        self.nestedRefPoset = GradedPosetSequence(self.nestedSeq, isGraded=True)
        self.unhashedPoset = GradedPosetSequence(self.sequence, hashableElements=True)
        self.unhashedNestedPoset = GradedPosetSequence(self.nestedSeq, isGraded=True, hashableElements=True)

    def test__init__(self):        
        sequence = range(10)
        nestedSeq = [[x] for x in xrange(8)] + [[8,9]]
        refPoset = GradedPosetSequence(sequence)
        unnestedGraded = GradedPosetSequence(self.sequence, isGraded=True)
        nestedRefPoset = GradedPosetSequence(nestedSeq, isGraded=True)
        unhasedPoset = GradedPosetSequence(nestedSeq, isGraded=True, hashableElements=True)

    def test__init__Errors(self):
        x = GradedPosetSequence([dict(),1], hashableElements=True)
        y = GradedPosetSequence([[dict()], [1]], isGraded=True, hashableElements=True)
        self.assertRaises(TypeError, x.inversions, [1])
        self.assertRaises(TypeError, y.inversions, [1])

    def test__len__(self):
        self.assertEqual(len(self.refPoset), len(self.sequence))
        self.assertEqual(len(self.nestedRefPoset), len(self.nestedSeq))

    def test__iter__(self):
        for i, x in enumerate(self.refPoset):
            self.assertEqual(x, self.sequence[i])
        for i, x in enumerate(self.nestedRefPoset):
            self.assertEqual(x, self.nestedSeq[i])

    def testIterElements(self):
        for i, x in enumerate(self.refPoset.iterElements()):
            self.assertEqual(x, self.sequence[i])

    def testIterElements_Graded(self):
        flatSeq = [x for subseq in self.nestedSeq for x in subseq]
        for i, x in enumerate(self.nestedRefPoset.iterElements()):
            self.assertEqual(x, flatSeq[i])

    def testMaxInversions(self):
        self.assertEqual(45, self.refPoset.maxInversions(self.sequence))
        self.assertEqual(44, self.refPoset.maxInversions(self.nestedSeq, isGraded=True))
        self.assertEqual(44, self.nestedRefPoset.maxInversions(self.sequence))
        self.assertEqual(44, self.nestedRefPoset.maxInversions(self.nestedSeq, isGraded=True))
        self.assertEqual(45, self.unhashedPoset.maxInversions(self.sequence))
        self.assertEqual(44, self.unhashedPoset.maxInversions(self.nestedSeq, isGraded=True))
        self.assertEqual(44, self.unhashedNestedPoset.maxInversions(self.sequence))
        self.assertEqual(44, self.unhashedNestedPoset.maxInversions(self.nestedSeq, isGraded=True))

    def testMean(self):
        self.assertEqual(22.5, self.refPoset.mean(self.sequence))
        self.assertEqual(22, self.refPoset.mean(self.nestedSeq, isGraded=True))
        self.assertEqual(22, self.nestedRefPoset.mean(self.sequence))
        self.assertEqual(22, self.nestedRefPoset.mean(self.nestedSeq, isGraded=True))
        self.assertEqual(22.5, self.unhashedPoset.mean(self.sequence))
        self.assertEqual(22, self.unhashedPoset.mean(self.nestedSeq, isGraded=True))
        self.assertEqual(22, self.unhashedNestedPoset.mean(self.sequence))
        self.assertEqual(22, self.unhashedNestedPoset.mean(self.nestedSeq, isGraded=True))

    def testVariance(self):
        self.assertEqual(31.25, self.refPoset.variance(self.sequence))
        self.assertEqual(31, self.refPoset.variance(self.nestedSeq, isGraded=True))
        self.assertEqual(31, self.nestedRefPoset.variance(self.sequence))
        self.assertEqual(31, self.nestedRefPoset.variance(self.nestedSeq, isGraded=True))
        self.assertEqual(31.25, self.unhashedPoset.variance(self.sequence))
        self.assertEqual(31, self.unhashedPoset.variance(self.nestedSeq, isGraded=True))
        self.assertEqual(31, self.unhashedNestedPoset.variance(self.sequence))
        self.assertEqual(31, self.unhashedNestedPoset.variance(self.nestedSeq, isGraded=True))

    def testStdDev(self):
        self.assertEqual(31.25**0.5, self.refPoset.stdDev(self.sequence))
        self.assertEqual(31**0.5, self.refPoset.stdDev(self.nestedSeq, isGraded=True))
        self.assertEqual(31**0.5, self.nestedRefPoset.stdDev(self.sequence))
        self.assertEqual(31**0.5, self.nestedRefPoset.stdDev(self.nestedSeq, isGraded=True))
        self.assertEqual(31.25**0.5, self.unhashedPoset.stdDev(self.sequence))
        self.assertEqual(31**0.5, self.unhashedPoset.stdDev(self.nestedSeq, isGraded=True))
        self.assertEqual(31**0.5, self.unhashedNestedPoset.stdDev(self.sequence))
        self.assertEqual(31**0.5, self.unhashedNestedPoset.stdDev(self.nestedSeq, isGraded=True))

    def testInversions(self):
        # Same thing
        self.assertEqual(0, self.refPoset.inversions(self.sequence))
        self.assertEqual(0, self.refPoset.inversions(self.nestedSeq, isGraded=True))
        self.assertEqual(0, self.nestedRefPoset.inversions(self.sequence))
        self.assertEqual(0, self.nestedRefPoset.inversions(self.nestedSeq, isGraded=True))
        self.assertEqual(0, self.unhashedPoset.inversions(self.sequence))
        self.assertEqual(0, self.unhashedPoset.inversions(self.nestedSeq, isGraded=True))
        self.assertEqual(0, self.unhashedNestedPoset.inversions(self.sequence))
        self.assertEqual(0, self.unhashedNestedPoset.inversions(self.nestedSeq, isGraded=True))
        # Reversed
        self.assertEqual(45, self.refPoset.inversions(self.reversedSeq))
        self.assertEqual(44, self.refPoset.inversions(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(44, self.nestedRefPoset.inversions(self.reversedSeq))
        self.assertEqual(44, self.nestedRefPoset.inversions(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(45, self.unhashedPoset.inversions(self.reversedSeq))
        self.assertEqual(44, self.unhashedPoset.inversions(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(44, self.unhashedNestedPoset.inversions(self.reversedSeq))
        self.assertEqual(44, self.unhashedNestedPoset.inversions(self.reversedNestedSeq, isGraded=True))

    def testSimilarity(self):
        # Same thing
        self.assertEqual(1, self.refPoset.similarity(self.sequence))
        self.assertEqual(1, self.refPoset.similarity(self.nestedSeq, isGraded=True))
        self.assertEqual(1, self.nestedRefPoset.similarity(self.sequence))
        self.assertEqual(1, self.nestedRefPoset.similarity(self.nestedSeq, isGraded=True))
        self.assertEqual(1, self.unhashedPoset.similarity(self.sequence))
        self.assertEqual(1, self.unhashedPoset.similarity(self.nestedSeq, isGraded=True))
        self.assertEqual(1, self.unhashedNestedPoset.similarity(self.sequence))
        self.assertEqual(1, self.unhashedNestedPoset.similarity(self.nestedSeq, isGraded=True))
        # Reversed
        self.assertEqual(0, self.refPoset.similarity(self.reversedSeq))
        self.assertEqual(0, self.refPoset.similarity(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(0, self.nestedRefPoset.similarity(self.reversedSeq))
        self.assertEqual(0, self.nestedRefPoset.similarity(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(0, self.unhashedPoset.similarity(self.reversedSeq))
        self.assertEqual(0, self.unhashedPoset.similarity(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(0, self.unhashedNestedPoset.similarity(self.reversedSeq))
        self.assertEqual(0, self.unhashedNestedPoset.similarity(self.reversedNestedSeq, isGraded=True))

    def testCorrelation(self):
        # Same thing
        self.assertEqual(1, self.refPoset.correlation(self.sequence))
        self.assertEqual(1, self.refPoset.correlation(self.nestedSeq, isGraded=True))
        self.assertEqual(1, self.nestedRefPoset.correlation(self.sequence))
        self.assertEqual(1, self.nestedRefPoset.correlation(self.nestedSeq, isGraded=True))
        self.assertEqual(1, self.unhashedPoset.correlation(self.sequence))
        self.assertEqual(1, self.unhashedPoset.correlation(self.nestedSeq, isGraded=True))
        self.assertEqual(1, self.unhashedNestedPoset.correlation(self.sequence))
        self.assertEqual(1, self.unhashedNestedPoset.correlation(self.nestedSeq, isGraded=True))
        # Reversed
        self.assertEqual(-1, self.refPoset.correlation(self.reversedSeq))
        self.assertEqual(-1, self.refPoset.correlation(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(-1, self.nestedRefPoset.correlation(self.reversedSeq))
        self.assertEqual(-1, self.nestedRefPoset.correlation(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(-1, self.unhashedPoset.correlation(self.reversedSeq))
        self.assertEqual(-1, self.unhashedPoset.correlation(self.reversedNestedSeq, isGraded=True))
        self.assertEqual(-1, self.unhashedNestedPoset.correlation(self.reversedSeq))
        self.assertEqual(-1, self.unhashedNestedPoset.correlation(self.reversedNestedSeq, isGraded=True))

    def testCdf(self):
        precision = 3
        for cdfType in CDF_TYPES:
            # Same thing
            self.assertAlmostEqual(0, self.refPoset.cdf(self.sequence, cdfType=cdfType), precision)
            self.assertAlmostEqual(0, self.refPoset.cdf(self.nestedSeq, isGraded=True, cdfType=cdfType), precision)
            self.assertAlmostEqual(0, self.nestedRefPoset.cdf(self.sequence, cdfType=cdfType), precision)
            self.assertAlmostEqual(0, self.nestedRefPoset.cdf(self.nestedSeq, isGraded=True, cdfType=cdfType), precision)
            self.assertAlmostEqual(0, self.unhashedPoset.cdf(self.sequence, cdfType=cdfType), precision)
            self.assertAlmostEqual(0, self.unhashedPoset.cdf(self.nestedSeq, isGraded=True, cdfType=cdfType), precision)
            self.assertAlmostEqual(0, self.unhashedNestedPoset.cdf(self.sequence, cdfType=cdfType), precision)
            self.assertAlmostEqual(0, self.unhashedNestedPoset.cdf(self.nestedSeq, isGraded=True, cdfType=cdfType), precision)
            # Reversed
            self.assertAlmostEqual(1, self.refPoset.cdf(self.reversedSeq, cdfType=cdfType), precision)
            self.assertAlmostEqual(1, self.refPoset.cdf(self.reversedNestedSeq, isGraded=True, cdfType=cdfType), precision)
            self.assertAlmostEqual(1, self.nestedRefPoset.cdf(self.reversedSeq, cdfType=cdfType), precision)
            self.assertAlmostEqual(1, self.nestedRefPoset.cdf(self.reversedNestedSeq, isGraded=True, cdfType=cdfType), precision)
            self.assertAlmostEqual(1, self.unhashedPoset.cdf(self.reversedSeq, cdfType=cdfType), precision)
            self.assertAlmostEqual(1, self.unhashedPoset.cdf(self.reversedNestedSeq, isGraded=True, cdfType=cdfType), precision)
            self.assertAlmostEqual(1, self.unhashedNestedPoset.cdf(self.reversedSeq, cdfType=cdfType), precision)
            self.assertAlmostEqual(1, self.unhashedNestedPoset.cdf(self.reversedNestedSeq, isGraded=True, cdfType=cdfType), precision)

    def testExactCDF(self):
        precision = 5
        # Same thing
        self.assertAlmostEqual(0, self.refPoset.exactCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.refPoset.exactCDF(self.nestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(0, self.nestedRefPoset.exactCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.nestedRefPoset.exactCDF(self.nestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(0, self.unhashedPoset.exactCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.unhashedPoset.exactCDF(self.nestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(0, self.unhashedNestedPoset.exactCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.unhashedNestedPoset.exactCDF(self.nestedSeq, isGraded=True), precision)
        # Reversed
        self.assertAlmostEqual(1, self.refPoset.exactCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.refPoset.exactCDF(self.reversedNestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(1, self.nestedRefPoset.exactCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.nestedRefPoset.exactCDF(self.reversedNestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(1, self.unhashedPoset.exactCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.unhashedPoset.exactCDF(self.reversedNestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(1, self.unhashedNestedPoset.exactCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.unhashedNestedPoset.exactCDF(self.reversedNestedSeq, isGraded=True), precision)

    def testNormalCDF(self):
        precision = 3
        # Same thing
        self.assertAlmostEqual(0, self.refPoset.normalCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.refPoset.normalCDF(self.nestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(0, self.nestedRefPoset.normalCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.nestedRefPoset.normalCDF(self.nestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(0, self.unhashedPoset.normalCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.unhashedPoset.normalCDF(self.nestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(0, self.unhashedNestedPoset.normalCDF(self.sequence), precision)
        self.assertAlmostEqual(0, self.unhashedNestedPoset.normalCDF(self.nestedSeq, isGraded=True), precision)
        # Reversed
        self.assertAlmostEqual(1, self.refPoset.normalCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.refPoset.normalCDF(self.reversedNestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(1, self.nestedRefPoset.normalCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.nestedRefPoset.normalCDF(self.reversedNestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(1, self.unhashedPoset.normalCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.unhashedPoset.normalCDF(self.reversedNestedSeq, isGraded=True), precision)
        self.assertAlmostEqual(1, self.unhashedNestedPoset.normalCDF(self.reversedSeq), precision)
        self.assertAlmostEqual(1, self.unhashedNestedPoset.normalCDF(self.reversedNestedSeq, isGraded=True), precision)

    def testSignTest(self):
        refList = range(10)
        nestedRef = [[val] for val in refList]
        refPoset = GradedPosetSequence(refList)
        nestedRefPoset = GradedPosetSequence(nestedRef, True)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        signs1 = [inversionCount(x) < inversionCountMean(x) for x in permutations1 if
                  inversionCount(x) != inversionCountMean(x)]
        signs2 = [inversionCount(x) < inversionCountMean(x) for x in permutations2 if
                  inversionCount(x) != inversionCountMean(x)]
        # Sign Test Comparison
        vals1 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations1]
        vals2 = [1.0-float(inversionCount(x))/inversionCountMax(x) for x in permutations2]
        self.assertEqual(refPoset.signTest(permutations1),
                         signTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.signTest(permutations2),
                         signTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.signTest(nestedPerm1, isGraded=True),
                         signTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.signTest(nestedPerm2, isGraded=True),
                         signTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        # Nested Tests
        self.assertEqual(nestedRefPoset.signTest(permutations1),
                         signTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(nestedRefPoset.signTest(permutations2),
                         signTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(nestedRefPoset.signTest(nestedPerm1, isGraded=True),
                         signTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(nestedRefPoset.signTest(nestedPerm2, isGraded=True),
                         signTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))

    def testWilcoxonSignedRankTest(self):
        refList = range(10)
        refPoset = GradedPosetSequence(refList)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        signs1 = [inversionCount(x) < inversionCountMean(x) for x in permutations1 if
                  inversionCount(x) != inversionCountMean(x)]
        signs2 = [inversionCount(x) < inversionCountMean(x) for x in permutations2 if
                  inversionCount(x) != inversionCountMean(x)]
        # Wilcoxon Tests
        vals1 = [1.0-inversionCountCDF(x) for x in permutations1]
        vals2 = [1.0-inversionCountCDF(x) for x in permutations2]
        self.assertEqual(refPoset.wilcoxonTest(permutations1),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.wilcoxonTest(permutations2),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.wilcoxonTest(permutations1, alternative=LESS_THAN_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=LESS_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.wilcoxonTest(permutations2, alternative=LESS_THAN_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=LESS_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.wilcoxonTest(permutations1, alternative=TWO_SIDED_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=TWO_SIDED_HYPOTHESIS))
        self.assertEqual(refPoset.wilcoxonTest(permutations2, alternative=TWO_SIDED_HYPOTHESIS),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=TWO_SIDED_HYPOTHESIS)) 
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPoset = GradedPosetSequence(nestedRef, isGraded=True)
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertEqual(nestedPoset.wilcoxonTest(nestedPerm1, isGraded=True),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(nestedPoset.wilcoxonTest(nestedPerm2, isGraded=True),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(nestedPoset.wilcoxonTest(permutations1, isGraded=False),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(nestedPoset.wilcoxonTest(permutations2),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.wilcoxonTest(nestedPerm1, isGraded=True),
                         wilcoxonSignedRankTest(vals1, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))
        self.assertEqual(refPoset.wilcoxonTest(nestedPerm2, isGraded=True),
                         wilcoxonSignedRankTest(vals2, mu=0.5, alternative=GREATER_THAN_HYPOTHESIS))

    def testPermutationMeanTest(self):
        refList = range(10)
        refPoset = GradedPosetSequence(refList)
        places = 2
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        #GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        # Original Test Comparison
        vals1 = [1.0-inversionCountCDF(x) for x in permutations1]
        vals2 = [1.0-inversionCountCDF(x) for x in permutations2]
        
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations1, permutations2),
                               permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations2, permutations1),
                         permutationMeanTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations1, permutations2, 
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationMeanTest(vals1, vals2, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations2, permutations1, 
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationMeanTest(vals2, vals1, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations1, permutations2,
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationMeanTest(vals1, vals2, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations2, permutations1,
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationMeanTest(vals2, vals1, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations1, permutations2,
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationMeanTest(vals1, vals2, TWO_SIDED_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations2, permutations1,
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationMeanTest(vals2, vals1, TWO_SIDED_HYPOTHESIS), places)
        
        # No Reference sequence
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations1, permutations2),
                         permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations2, permutations1),
                         permutationMeanTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPoset = GradedPosetSequence(nestedRef, isGraded=True)
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertAlmostEqual(nestedPoset.permutationMeanTest(nestedPerm1, nestedPerm2, isGraded=True),
                         permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(nestedPoset.permutationMeanTest(nestedPerm2, nestedPerm1, isGraded=True),
                         permutationMeanTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        # Params Tests
        self.assertAlmostEqual(refPoset.permutationMeanTest(permutations1, permutations2, 
                                                            isGraded=False,
                                                            measure=ADAPTIVE_CDF, pValue=0.8,
                                                            iterations=10000, useStoppingRule=False,
                                                            maxExactN=10),
                               permutationMeanTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS,
                                                   pValue=0.8, iterations=10000, useStoppingRule=False,
                                                   maxExactN=10), places)

    def testPermutationRankTest(self):
        places = 2
        refList = range(10)
        refPoset = GradedPosetSequence(refList)
        permutations1 = [range(10),
                         [9] + range(9),
                         range(5) + sorted(range(5,10), reverse=True),
                         range(4) + sorted(range(4,10), reverse=True),
                         [9,8] + range(7),
                         [8,9] + range(7),
                         range(10),
                         range(10)]
        permutations2 = [list(reversed(x)) for x in permutations1]
        #GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS
        # Original Test Comparison
        vals1 = [1.0-inversionCountCDF(x) for x in permutations1]
        vals2 = [1.0-inversionCountCDF(x) for x in permutations2]
        
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations1, permutations2),
                               permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations2, permutations1),
                         permutationRankTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        self.assertAlmostEqual(refPoset.permutationRankTest(permutations1, permutations2, 
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationRankTest(vals1, vals2, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations2, permutations1, 
                                                      alternative=GREATER_THAN_HYPOTHESIS),
                         permutationRankTest(vals2, vals1, GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations1, permutations2, 
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationRankTest(vals1, vals2, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations2, permutations1, 
                                                      alternative=LESS_THAN_HYPOTHESIS),
                         permutationRankTest(vals2, vals1, LESS_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations1, permutations2, 
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationRankTest(vals1, vals2, TWO_SIDED_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations2, permutations1, 
                                                      alternative=TWO_SIDED_HYPOTHESIS),
                         permutationRankTest(vals2, vals1, TWO_SIDED_HYPOTHESIS), places)
        
        # No Reference sequence
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations1, permutations2),
                         permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations2, permutations1),
                         permutationRankTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)
        # Nested Tests
        nestedRef = [[val] for val in refList]
        nestedPoset = GradedPosetSequence(nestedRef, isGraded=True)
        nestedPerm1 = [[[val] for val in x] for x in permutations1]
        nestedPerm2 = [[[val] for val in x] for x in permutations2]
        self.assertAlmostEqual(nestedPoset.permutationRankTest(nestedPerm1, nestedPerm2, isGraded=True),
                         permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS), places)
        self.assertAlmostEqual(nestedPoset.permutationRankTest(nestedPerm2, nestedPerm1, isGraded=True),
                         permutationRankTest(vals2, vals1, alternative=GREATER_THAN_HYPOTHESIS), places)

        # Params Tests
        self.assertAlmostEqual(refPoset.permutationRankTest(permutations1, permutations2, 
                                                            isGraded=False,
                                                            measure=ADAPTIVE_CDF, pValue=0.8,
                                                            iterations=10000, useStoppingRule=False,
                                                            maxExactN=10),
                               permutationRankTest(vals1, vals2, alternative=GREATER_THAN_HYPOTHESIS,
                                                   pValue=0.8, iterations=10000, useStoppingRule=False,
                                                   maxExactN=10), places)
 

    def test_calcGradedStatistic(self):
        mulitpleNest = [[0,1,2],[3,4],[5,6],[7,8,9]]
        def lenMinOne(x):
            return max(0,x-1)
        self.assertEqual(9, self.refPoset._calcGradedStatistic(lenMinOne))
        self.assertEqual(9, self.refPoset._calcGradedStatistic(lenMinOne, self.sequence))
        self.assertEqual(8, self.nestedRefPoset._calcGradedStatistic(lenMinOne))
        self.assertEqual(8, self.nestedRefPoset._calcGradedStatistic(lenMinOne, self.sequence))
        self.assertEqual(8, self.nestedRefPoset._calcGradedStatistic(lenMinOne, self.nestedSeq, True))
        self.assertEqual(3, self.nestedRefPoset._calcGradedStatistic(lenMinOne, mulitpleNest, True))

    def test_calcNumElements(self):
        self.assertEqual(10, GradedPosetSequence._calcNumElements(self.sequence, isGraded=False))
        self.assertEqual(10, GradedPosetSequence._calcNumElements(self.nestedSeq, isGraded=True))

    def test_calcOverloadedRanks(self):
        hashableRef = GradedPosetSequence(range(10))
        unhashableRef = GradedPosetSequence(range(10), hashableElements=False)
        nested = [[x] for x in xrange(8)] + [[8,9]]
        nestedRef = GradedPosetSequence(nested, True)
        self.assertEqual([], hashableRef._calcOverloadedRanks(range(10), False))
        self.assertEqual([], unhashableRef._calcOverloadedRanks(range(10), False))
        self.assertEqual([[8,9]], hashableRef._calcOverloadedRanks(nested, True))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True, range(10), False))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True, nested, True))
        self.assertEqual([[8,9]], hashableRef._calcOverloadedRanks(nestedRef, True))
        self.assertEqual([], unhashableRef._calcOverloadedRanks(nested, True, range(9)))
        
    def test_calcOverloadedRanks_MinimalGrades(self):
        hashableRef = GradedPosetSequence(range(10))
        unhashableRef = GradedPosetSequence(range(10), hashableElements=False)
        nested = [x for x in xrange(8)] + [[8,9]]
        nestedRef = GradedPosetSequence(nested, True)
        self.assertEqual([], hashableRef._calcOverloadedRanks(range(10), False))
        self.assertEqual([], unhashableRef._calcOverloadedRanks(range(10), False))
        self.assertEqual([[8,9]], hashableRef._calcOverloadedRanks(nested, True))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True, range(10), False))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True, nested, True))
        self.assertEqual([[8,9]], hashableRef._calcOverloadedRanks(nestedRef, True))
        self.assertEqual([], unhashableRef._calcOverloadedRanks(nested, True, range(9)))

    def test_calcOverloadedRanks_Posets(self):
        hashableRef = GradedPosetSequence(range(10))
        unhashableRef = GradedPosetSequence(range(10), hashableElements=False)
        nested = GradedPosetSequence([x for x in xrange(8)] + [[8,9]], isGraded=True)
        nestedRef = GradedPosetSequence(nested._sequence, True)
        self.assertEqual([], hashableRef._calcOverloadedRanks(GradedPosetSequence(range(10)), False))
        self.assertEqual([], unhashableRef._calcOverloadedRanks(GradedPosetSequence(range(10)), False))
        self.assertEqual([[8,9]], hashableRef._calcOverloadedRanks(nested, True))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True, range(10), False))
        self.assertEqual([[8,9]], unhashableRef._calcOverloadedRanks(nested, True, nested, True))
        self.assertEqual([[8,9]], hashableRef._calcOverloadedRanks(nestedRef, True))
        self.assertEqual([], unhashableRef._calcOverloadedRanks(nested, True, range(9)))


    def test_calcRankIntersections(self):
        hashableRef = GradedPosetSequence(range(10))
        unhashableRef = GradedPosetSequence(range(10), hashableElements=False)
        def doubleSorted(seq):
            for x in seq:
                x.sort()
            seq.sort()
            return seq
        self.assertEqual([], hashableRef._calcRankIntersections([], []))
        self.assertEqual([], hashableRef._calcRankIntersections([[1,2]], [[3,4]]))
        self.assertEqual([[1,2]], doubleSorted(hashableRef._calcRankIntersections([[1,2]], [[1,2]])))
        self.assertEqual([[1,2]], doubleSorted(hashableRef._calcRankIntersections([[1,2]], [[1,2,3], [4,5]])))
        self.assertEqual(doubleSorted([[1,2],[4,5]]),
                         doubleSorted(hashableRef._calcRankIntersections([[1,2,4,5]], [[1,2,3], [4,5]])))
        self.assertEqual(doubleSorted([[1,2],[4,5]]),
                         doubleSorted(hashableRef._calcRankIntersections([[1,2,4,5]], [[1,2,3], [4,5]])))
        self.assertEqual(doubleSorted([[4,5], [2,3], [6,9]]),
                         doubleSorted(hashableRef._calcRankIntersections([[1,4,5],[2,3,6,9]], [[1,2,3], [4,5], [6,9]])))

    def testValidate(self):
        self.refPoset.validate()
        self.nestedRefPoset.validate()
        self.unhashedPoset.validate()
        self.unhashedNestedPoset.validate()
        # Invalide Posets
        invalidPoset = GradedPosetSequence([[1,2],[1]], isGraded=True)
        invalidPoset2 = GradedPosetSequence([set()], hashableElements=True)
        invalidPoset3 = GradedPosetSequence([1,1,1,2,3,4,4])
        invalidPoset4 = GradedPosetSequence([1,1,1,2,3,4,4, set(), dict(), set()])
        self.assertRaises(InvalidGradedPosetError, invalidPoset.validate)
        self.assertRaises(InvalidGradedPosetError, invalidPoset2.validate)
        self.assertRaises(InvalidGradedPosetError, invalidPoset3.validate)
        self.assertRaises(InvalidGradedPosetError, invalidPoset4.validate)

if __name__ == "__main__":
    unittest.main()
