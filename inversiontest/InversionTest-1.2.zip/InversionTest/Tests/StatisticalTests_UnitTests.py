import unittest.case
from random import shuffle
from InversionTest.StatisticalTests import (
    absAndValKey, genericSymmetricPairedTest,
    pythonNormalCDF, normalCDFFunction,
    binomialTest, pythonBinomialTest, pythonSignTestStatistic, 
    pythonWilcoxonSignedRankStatistic, scipyWilcoxonStatistic, signTest, 
    wilcoxonSignedRankStatistic, wilcoxonSignedRankTest, wilcoxonMeanScore,
    scipyBinomialTestStatistic, transformSymmetricPValueHypothesis,
    GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS,
    SignTestInvalidPairLengthError, SignTestCancelationError,
    IS_SCIPY_AVAILABLE, permutationTest, permutationMeanTest,
    permutationRankTest)

class StatisticalTests_FunctionsTest(unittest.case.TestCase):
    VERBOSE = False

    # Normal Test Cases
    #---------------------------------------------
    NUM_PLACES = 4
                             # Test cases in form: mean, var, value, cdf(value)
    NORMAL_TEST_VALUES  =   ((0,   1,      -1,     0.1587),
                             (0.0, 1.0,    -1.0,   0.1587),
                             (0.0, 1.0,     0.0,   0.5000),
                             (0.0, 1.0,     1.0,   0.8413),
                             # Tests w/ Mean=1
                             (1.0, 1.0,     0.0,   0.1587),
                             (1.0, 1.0,     1.0,   0.5000),
                             (1.0, 1.0,     2.0,   0.8413),
                             # Tests w/ Var=2
                             (0.0, 2.0,    -2.0,   0.1587),
                             (0.0, 2.0,     0.0,   0.5000),
                             (0.0, 2.0,     2.0,   0.8413),)

    # Binomial Comparison Values (from R binom.exact)
    # In form: (x, n, p), pValue
    #----------------------------------------------
    BINOMIAL_TWO_TAIL=  (((99, 200, 0.5),  0.9437),
                         ((45, 100, 0.5),  0.3682),
                         ((65, 100, 0.5),  0.0035),
                         ((8,   12, 0.5),  0.3877),
                         ((3,   12, 0.5),  0.1460),
                         ((99, 200, 0.05), 0.0000),
                         ((5,  100, 0.05), 1.0000),
                         ((65, 100, 0.05), 0.0000),
                         ((8,   12, 0.05), 0.0000),
                         ((3,   12, 0.05), 0.01957))

    BINOMIAL_LESS_THAN= (((99, 200, 0.5),  0.4718),
                         ((45,  100, 0.5), 0.1841),
                         ((65, 100, 0.5),  0.9991),
                         ((8,   12, 0.5),  0.9270),
                         ((3,   12, 0.5),  0.0730),
                         ((99, 200, 0.05), 1.0000),
                         ((5,  100, 0.05), 0.6160),
                         ((65, 100, 0.05), 1.0000),
                         ((8,   12, 0.05), 1.0000),
                         ((3,   12, 0.05), 0.9978))

    BINOMIAL_GREATER=   (((99, 200, 0.5),  0.5840),
                         ((45, 100, 0.5),  0.8644),
                         ((65, 100, 0.5),  0.001759),
                         ((8,   12, 0.5),  0.1938),
                         ((3,   12, 0.5),  0.9807),
                         ((99, 200, 0.05), 0.0000),
                         ((5,  100, 0.05), 0.5640),
                         ((65, 100, 0.05), 0.0000),
                         ((8,   12, 0.05), 0.0000),
                         ((3,   12, 0.05), 0.01957))

    # Critical Values for p=0.5, where two-sided p=2.0*min(p_upper, p_lower)
    # Params: n, two-tail < 0.05, two-tail < 0.01, one-tail < 0.05, one-tail < 0.01
    # Note: These are not used by default, as the two-sided is calculated using "minlike" like R and SciPy
    #----------------------------------------------
    BINOMIAL_CRITICAL_VALUES = (
                            (5, (None,None), (None,None), (0,5), (None, None)),
                            (6, (0,6), (None,None), (0,6), (None, None)),
                            (7, (0,7), (None,None), (0,7), (0,7)),
                            (8, (0, 8), (0, 8), (1 , 7), ( 0 , 8)),
                            (9, (1, 8), (0, 9), (1 , 8), ( 0 , 9)),
                            (10,(1, 9), (0, 10), (1 , 9), ( 0 , 10)),
                            (11,(1, 10), (0, 11), (2 , 9), ( 1 , 10)),
                            (12,(2, 10), (1, 11), (2 , 10), ( 1 , 11)),
                            (13, (2, 11), (1, 12), (3 , 10), ( 1 , 12)),
                            (14, (2, 12), (1, 13), (3 , 11), ( 2 , 12)),
                            (15, (3, 12), (2, 13), (3 , 12), ( 2 , 13)),
                            (16, (3, 13), (2, 14), (4 , 12), ( 2 , 14)),
                            (17, (4, 13), (2, 15), (4 , 13), ( 3 , 14)),
                            (18, (4, 14), (3, 15), (5 , 13), ( 3 , 15)),
                            (19, (4, 15), (3, 16), (5 , 14), ( 4 , 15)),
                            (20, (5, 15), (3, 17), (5 , 15), ( 4 , 16)),
                            (21, (5, 16), (4, 17), (6 , 15), ( 4 , 17)),
                            (22, (5, 17), (4, 18), (6 , 16), ( 5 , 17)),
                            (23, (6, 17), (4, 19), (7 , 16), ( 5 , 18)),
                            (24, (6, 18), (5, 19), (7 , 17), ( 5 , 19)),
                            (25, (7, 18), (5, 20), (7 , 18), ( 6 , 19)),
                            (26, (7, 19), (6, 20), (8 , 18), ( 6 , 20)),
                            (27, (7, 20), (6, 21), (8 , 19), ( 7 , 20)),
                            (28, (8, 20), (6, 22), (9 , 19), ( 7 , 21)),
                            (29, (8, 21), (7, 22), (9 , 20), ( 7 , 22)),
                            (30, (9, 21), (7, 23), (10 , 20), ( 8 , 22)),
                            (31, (9, 22), (7, 24), (10 , 21), ( 8 , 23)),
                            (32, (9, 23), (8, 24), (10 , 22), ( 8 , 24)),
                            (33, (10, 23), (8, 25), (11 , 22), ( 9 , 24)),
                            (34, (10, 24), (9, 25), (11 , 23), ( 9 , 25)),
                            (35, (11, 24), (9, 26), (12 , 23), ( 10 , 25)),
                            (36, (11, 25), (9, 27), (12 , 24), ( 10 , 26)),
                            (37, (12, 25), (10, 27), (13 , 24), ( 10 , 27)),
                            (38, (12, 26), (10, 28), (13 , 25), ( 11 , 27)),
                            (39, (12, 27), (11, 28), (13 , 26), ( 11 , 28)),
                            (40, (13, 27), (11, 29), (14 , 26), ( 12 , 28)))

    # Wilcoxon Comparison Data ((from R wilcox.test with exact=FALSE)
    # In form: (x, y, mu), wStat, pValue
    #----------------------------------------------
    WILCOXON_TWO_SIDED = (((range(0,21), None, 10),  105, 1.0),
                          ((range(0,21), None, 16.5), 18, 0.0006992),
                          ((range(0,21), None, 7.5), 163, 0.09854))

    WILCOXON_GREATER =   (((range(0,21), None, 10),  105, 0.5),
                          ((range(0,21), None, 16.5), 18, 0.9997),
                          ((range(0,21), None, 7.5), 163, 0.04927))

    WILCOXON_LESS =     (((range(0,21), None, 10),  105, 0.5),
                          ((range(0,21), None, 16.5), 18, 0.0003496),
                          ((range(0,21), None, 7.5), 163, 0.9507))

    # Permutation t-Test Comparison Data
    # In form: (x, y), pValue
    #-----------------------------------------------------
    PERMUTATION_T_TWO_SIDED = ((((1,2,3,4), (3,4,5,6)), 0.1429),
                               (((1,2,3,4), (1,2,3,4)), 1.0),
                               (((4,3,2,1), (1,2,3,4)), 1.0),
                               (((1,2,3,4), (4,3,2,1)), 1.0))

    PERMUTATION_T_GREATER = ((((1,2,3,4), (3,4,5,6)), 0.9857),
                             (((1,2,3,4), (1,2,3,4)), 0.6286),
                             (((4,3,2,1), (1,2,3,4)), 0.6286),
                             (((1,2,3,4), (4,3,2,1)), 0.6286))

    PERMUTATION_T_LESS    = ((((1,2,3,4), (3,4,5,6)), 0.07143),
                             (((1,2,3,4), (1,2,3,4)), 0.6286),
                             (((4,3,2,1), (1,2,3,4)), 0.6286),
                             (((1,2,3,4), (4,3,2,1)), 0.6286))

    # Tests
    #--------------------------------------------------------
    def testAbsAndValKey_Positive(self):
        x = 5
        self.assertEqual(absAndValKey(x), (x, x))
        
    def testAbsAndValKey_Negative(self):
        x = -5
        self.assertEqual(absAndValKey(x), (-x, x))

    def testPermutationTest(self):
        def testStat(a, b, x=[]):
            x.append(1)
            return len(x)
        self.assertEqual(0.0, permutationTest(range(4), range(3,5), testStat))
        self.assertEqual(0.0, permutationTest(range(4), range(3,5), testStat, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(0.0, permutationTest(range(4), range(3,5), testStat, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(1.0, permutationTest(range(4), range(3,5), testStat, LESS_THAN_HYPOTHESIS))

    def testPermutationMeanTest_TwoSided(self):
        approxPrecision = 1
        approxFullPrecision = 2
        exactPrecision = 3
        alternate = TWO_SIDED_HYPOTHESIS
        data = self.PERMUTATION_T_TWO_SIDED
        for (x, y), pVal in data:
            exactVal = permutationMeanTest(x, y, alternate, maxExactN=None)
            approxFullVal = permutationMeanTest(x, y, alternate, useStoppingRule=False, iterations=100000)
            approxVal = permutationMeanTest(x, y, alternate, useStoppingRule=False, pValue=0.95, iterations=100000)
            if self.VERBOSE:
                print x, y, pVal
                print "Exact", exactVal
                print "Approx (Full)", approxFullVal
                print "Approx", approxVal
            self.assertAlmostEqual(pVal, exactVal, exactPrecision)
            self.assertAlmostEqual(pVal, approxFullVal, approxFullPrecision)
            self.assertAlmostEqual(pVal, approxVal, approxPrecision)
            
    def testPermutationMeanTest_GreaterThan(self):
        approxPrecision = 1
        approxFullPrecision = 2
        exactPrecision = 3
        alternate = GREATER_THAN_HYPOTHESIS
        data = self.PERMUTATION_T_GREATER
        for (x, y), pVal in data:
            exactVal = permutationMeanTest(x, y, alternate, maxExactN=None)
            approxFullVal = permutationMeanTest(x, y, alternate, useStoppingRule=False, iterations=100000)
            approxVal = permutationMeanTest(x, y, alternate, useStoppingRule=False, pValue=0.95, iterations=100000)
            if self.VERBOSE:
                print x, y, pVal
                print "Exact", exactVal
                print "Approx (Full)", approxFullVal
                print "Approx", approxVal
            self.assertAlmostEqual(pVal, exactVal, exactPrecision)
            self.assertAlmostEqual(pVal, approxFullVal, approxFullPrecision)
            self.assertAlmostEqual(pVal, approxVal, approxPrecision)
            
    def testPermutationMeanTest_LessThan(self):
        approxPrecision = 1
        approxFullPrecision = 2
        exactPrecision = 3
        alternate = LESS_THAN_HYPOTHESIS
        data = self.PERMUTATION_T_LESS
        for (x, y), pVal in data:
            exactVal = permutationMeanTest(x, y, alternate, maxExactN=None)
            approxFullVal = permutationMeanTest(x, y, alternate, useStoppingRule=False, iterations=100000)
            approxVal = permutationMeanTest(x, y, alternate, useStoppingRule=False, pValue=0.95, iterations=100000)
            if self.VERBOSE:
                print x, y, pVal
                print "Exact", exactVal
                print "Approx (Full)", approxFullVal
                print "Approx", approxVal
            self.assertAlmostEqual(pVal, exactVal, exactPrecision)
            self.assertAlmostEqual(pVal, approxFullVal, approxFullPrecision)
            self.assertAlmostEqual(pVal, approxVal, approxPrecision)
            
    def testPermutationRankTest_TwoSided(self):
        approxPrecision = 1
        approxFullPrecision = 2
        exactPrecision = 3
        alternate = TWO_SIDED_HYPOTHESIS
        data = self.PERMUTATION_T_TWO_SIDED
        for (x, y), pVal in data:
            exactVal = permutationRankTest(x, y, alternate, maxExactN=None)
            approxFullVal = permutationRankTest(x, y, alternate, useStoppingRule=False, iterations=100000)
            approxVal = permutationRankTest(x, y, alternate, useStoppingRule=False, pValue=0.95, iterations=100000)
            if self.VERBOSE:
                print x, y, pVal
                print "Exact", exactVal
                print "Approx (Full)", approxFullVal
                print "Approx", approxVal
            self.assertAlmostEqual(pVal, exactVal, exactPrecision)
            self.assertAlmostEqual(pVal, approxFullVal, approxFullPrecision)
            self.assertAlmostEqual(pVal, approxVal, approxPrecision)
            
    def testPermutationRankTest_GreaterThan(self):
        approxPrecision = 1
        approxFullPrecision = 2
        exactPrecision = 3
        alternate = GREATER_THAN_HYPOTHESIS
        data = self.PERMUTATION_T_GREATER
        for (x, y), pVal in data:
            exactVal = permutationRankTest(x, y, alternate, maxExactN=None)
            approxFullVal = permutationRankTest(x, y, alternate, useStoppingRule=False, iterations=100000)
            approxVal = permutationRankTest(x, y, alternate, useStoppingRule=False, pValue=0.95, iterations=100000)
            if self.VERBOSE:
                print x, y, pVal
                print "Exact", exactVal
                print "Approx (Full)", approxFullVal
                print "Approx", approxVal
            self.assertAlmostEqual(pVal, exactVal, exactPrecision)
            self.assertAlmostEqual(pVal, approxFullVal, approxFullPrecision)
            self.assertAlmostEqual(pVal, approxVal, approxPrecision)
            
    def testPermutationRankTest_LessThan(self):
        approxPrecision = 1
        approxFullPrecision = 2
        exactPrecision = 3
        alternate = LESS_THAN_HYPOTHESIS
        data = self.PERMUTATION_T_LESS
        for (x, y), pVal in data:
            exactVal = permutationRankTest(x, y, alternate, maxExactN=None)
            approxFullVal = permutationRankTest(x, y, alternate, useStoppingRule=False, iterations=100000)
            approxVal = permutationRankTest(x, y, alternate, useStoppingRule=False, pValue=0.95, iterations=100000)
            if self.VERBOSE:
                print x, y, pVal
                print "Exact", exactVal
                print "Approx (Full)", approxFullVal
                print "Approx", approxVal
            self.assertAlmostEqual(pVal, exactVal, exactPrecision)
            self.assertAlmostEqual(pVal, approxFullVal, approxFullPrecision)
            self.assertAlmostEqual(pVal, approxVal, approxPrecision)

    def testScipyNormalCDF(self):
        if not IS_SCIPY_AVAILABLE:
            self.fail("WARNING: Optional package <scipy> not available\n")
        from scipy.stats import norm
        normalFunction = norm.cdf
        for mean, var, x, expectedValue in self.NORMAL_TEST_VALUES:
            self.assertAlmostEqual(normalFunction(x, mean, var), expectedValue, self.NUM_PLACES)

    def testPythonNormalCDF(self):
        normalFunction = pythonNormalCDF
        for mean, var, x, expectedValue in self.NORMAL_TEST_VALUES:
            self.assertAlmostEqual(normalFunction(x, mean, var), expectedValue, self.NUM_PLACES)

    
    def testPythonNormalCDF(self):
        normalFunction = normalCDFFunction
        for mean, var, x, expectedValue in self.NORMAL_TEST_VALUES:
            self.assertAlmostEqual(normalFunction(x, mean, var), expectedValue, self.NUM_PLACES)


    def testPythonSignTestStatistic_MuEqual(self):
        x = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        mu = 0.5
        self.assertEqual(pythonSignTestStatistic(x, None, mu, TWO_SIDED_HYPOTHESIS),
                         binomialTest(3, 6, 0.5, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, None, mu, GREATER_THAN_HYPOTHESIS),
                         binomialTest(3, 6, 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, None, mu, LESS_THAN_HYPOTHESIS),
                         binomialTest(3, 6, 0.5, LESS_THAN_HYPOTHESIS))

    def testPythonSignTestStatistic_MuGreater(self):
        x = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        mu = 0.8
        self.assertEqual(pythonSignTestStatistic(x, None, mu, TWO_SIDED_HYPOTHESIS),
                         binomialTest(1, 5, 0.5, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, None, mu, GREATER_THAN_HYPOTHESIS),
                         binomialTest(1, 5, 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, None, mu, LESS_THAN_HYPOTHESIS),
                         binomialTest(1, 5, 0.5, LESS_THAN_HYPOTHESIS))

    def testPythonSignTestStatistic_MuLess(self):
        x = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 100]
        mu = 0.3
        self.assertEqual(pythonSignTestStatistic(x, None, mu, TWO_SIDED_HYPOTHESIS),
                         binomialTest(6, 8, 0.5, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, None, mu, GREATER_THAN_HYPOTHESIS),
                         binomialTest(6, 8, 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, None, mu, LESS_THAN_HYPOTHESIS),
                         binomialTest(6, 8, 0.5, LESS_THAN_HYPOTHESIS))

    def testPythonSignTestStatistic_SeriesEqual(self):
        x = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        y = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
        y2 = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        y3 = [1,2,3]
        self.assertEqual(pythonSignTestStatistic(x, y, alternative=TWO_SIDED_HYPOTHESIS),
                         binomialTest(3, 6, 0.5, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, y, alternative=GREATER_THAN_HYPOTHESIS),
                         binomialTest(3, 6, 0.5, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(pythonSignTestStatistic(x, y, alternative=LESS_THAN_HYPOTHESIS),
                         binomialTest(3, 6, 0.5, LESS_THAN_HYPOTHESIS))
        self.assertRaises(SignTestCancelationError, pythonSignTestStatistic,
                          x, y2, 0.5, TWO_SIDED_HYPOTHESIS)
        self.assertRaises(SignTestCancelationError, pythonSignTestStatistic,
                          x, y2, 0.5, GREATER_THAN_HYPOTHESIS)
        self.assertRaises(SignTestCancelationError, pythonSignTestStatistic,
                          x, y2, 0.5, LESS_THAN_HYPOTHESIS)
        self.assertRaises(SignTestInvalidPairLengthError, pythonSignTestStatistic,
                          x, y3, 0.5, LESS_THAN_HYPOTHESIS)

    def testSignTest(self):
        x = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        mu = 0.5
        self.assertEqual(signTest(x, None, mu), pythonSignTestStatistic(x, None, mu))

    def testWilcoxonSignedRankTest_TwoSided(self):
        test = wilcoxonSignedRankTest
        values = self.WILCOXON_TWO_SIDED
        for params, rWValue, rPValue in values:
            pValue = test(*params)
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testWilcoxonSignedRankTest_Greater(self):
        test = wilcoxonSignedRankTest
        values = self.WILCOXON_GREATER
        for params, rWValue, rPValue in values:
            pValue = test(*list(params)+[GREATER_THAN_HYPOTHESIS])
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testWilcoxonSignedRankTest_Less(self):
        test = wilcoxonSignedRankTest
        values = self.WILCOXON_LESS
        for params, rWValue, rPValue in values:
            pValue = test(*list(params)+[LESS_THAN_HYPOTHESIS])
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testWilcoxonSignedRankStatistic(self):
        test = wilcoxonSignedRankStatistic
        originTest = pythonWilcoxonSignedRankStatistic
        values = self.WILCOXON_TWO_SIDED
        for params, rWValue, rPValue in values:
            self.assertEqual(test(*params), originTest(*params))

    def testPythonWilcoxonSignedRankStatistic(self):
        test = pythonWilcoxonSignedRankStatistic
        values = self.WILCOXON_TWO_SIDED
        for params, rWValue, rPValue in values:
            wValue, pValue = test(*params)
            self.assertAlmostEqual(wValue, rWValue, 4)
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testScipyWilcoxonStatistic(self):
        if not IS_SCIPY_AVAILABLE:
            self.fail("WARNING: Optional package <scipy> not available\n")
        test = scipyWilcoxonStatistic
        values = self.WILCOXON_TWO_SIDED
        for params, rWValue, rPValue in values:
            rWValue = min(rWValue, wilcoxonMeanScore(*params)*2.0-rWValue)
            wValue, pValue = test(*params)
            self.assertAlmostEqual(wValue, rWValue, 2)
            #Note: SciPy and R do not agree about p-values for the same W value
            #self.assertAlmostEqual(pValue, rPValue, 2)

    def testWilcoxonMeanScore(self):
        # No Ties
        self.assertEqual(39, wilcoxonMeanScore(range(12), range(12,24)))
        self.assertEqual(39, wilcoxonMeanScore(range(12), mu=6.5))
        # One Tie
        self.assertEqual(33, wilcoxonMeanScore(range(12), range(12,0,-1)))
        self.assertEqual(33, wilcoxonMeanScore(range(12), mu=6))

    def testPythonBinomial_CriticalValues(self):
        p = 0.5
        test = pythonBinomialTest
        criticalValues = self.BINOMIAL_CRITICAL_VALUES
        for (n, (lowerTwoFifth, upperTwoFifth), (lowerTwoOneth, upperTwoOneth),
             (lowerOneFifth, upperOneFifth), (lowerOneOneth, upperOneOneth)) in criticalValues:
            c_lowerTwoFifth = None
            c_upperTwoFifth = None
            c_lowerTwoOneth = None
            c_upperTwoOneth = None
            c_lowerOneFifth = None
            c_upperOneFifth = None
            c_lowerOneOneth = None
            c_upperOneOneth = None
            for k in xrange(0, n+1):
                pTwo = test(k, n, p, TWO_SIDED_HYPOTHESIS, False)
                pOneLess = test(k, n, p, LESS_THAN_HYPOTHESIS, False)
                pOneGreater = test(k, n, p, GREATER_THAN_HYPOTHESIS, False) 
                if pTwo < 0.05  and k < n*p:
                    c_lowerTwoFifth = k
                if pTwo < 0.05 and k > n*p and c_upperTwoFifth is None:
                    c_upperTwoFifth = k
                if pTwo < 0.01 and k < n*p:
                    c_lowerTwoOneth = k
                if pTwo < 0.01 and k > n*p and c_upperTwoOneth is None:
                    c_upperTwoOneth = k
                if pOneLess < 0.05 and k < n*p:
                    c_lowerOneFifth = k
                if pOneGreater < 0.05 and k > n*p and c_upperOneFifth is None:
                    c_upperOneFifth = k
                if pOneLess < 0.01 and k < n*p:
                    c_lowerOneOneth = k
                if pOneGreater < 0.01 and k > n*p and c_upperOneOneth is None:
                    c_upperOneOneth = k
            self.assertEqual(lowerTwoFifth, c_lowerTwoFifth)
            self.assertEqual(upperTwoFifth, c_upperTwoFifth)
            self.assertEqual(lowerTwoOneth, c_lowerTwoOneth)
            self.assertEqual(upperTwoOneth, c_upperTwoOneth)
            self.assertEqual(lowerOneFifth, c_lowerOneFifth)
            self.assertEqual(upperOneFifth, c_upperOneFifth)
            self.assertEqual(lowerOneOneth, c_lowerOneOneth)
            self.assertEqual(upperOneOneth, c_upperOneOneth)
                
    def testPythonBinomialTest_TwoSided(self):
        test = pythonBinomialTest
        values = self.BINOMIAL_TWO_TAIL
        for params, rPValue in values:
            pValue = test(*params)
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testSciPyBinomialTest_TwoSided(self):
        if not IS_SCIPY_AVAILABLE:
            self.fail("WARNING: Optional package <scipy> not available\n")
        test = scipyBinomialTestStatistic
        values = self.BINOMIAL_TWO_TAIL
        for params, rPValue in values:
            pValue = test(*params)
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testPythonBinomialTest_Less(self):
        test = pythonBinomialTest
        values = self.BINOMIAL_LESS_THAN
        for params, rPValue in values:
            pValue = test(*list(params)+[LESS_THAN_HYPOTHESIS])
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testSciPyBinomialTest_Less(self):
        if not IS_SCIPY_AVAILABLE:
            self.fail("WARNING: Optional package <scipy> not available\n")
        test = scipyBinomialTestStatistic
        values = self.BINOMIAL_LESS_THAN
        for params, rPValue in values:
            pValue = test(*list(params)+[LESS_THAN_HYPOTHESIS])
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testPythonBinomialTest_Greater(self):
        test = pythonBinomialTest
        values = self.BINOMIAL_GREATER
        for params, rPValue in values:
            pValue = test(*list(params)+[GREATER_THAN_HYPOTHESIS])
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testSciPyBinomialTest_Greater(self):
        if not IS_SCIPY_AVAILABLE:
            self.fail("WARNING: Optional package <scipy> not available\n")
        test = scipyBinomialTestStatistic
        values = self.BINOMIAL_GREATER
        for params, rPValue in values:
            pValue = test(*list(params)+[GREATER_THAN_HYPOTHESIS])
            self.assertAlmostEqual(pValue, rPValue, 4)

    def testGenericSymmetricPairedTest_NoSeries2Equal(self):
        test = genericSymmetricPairedTest
        x = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        self.assertEqual(1.0, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, TWO_SIDED_HYPOTHESIS, x, mu=0.5))
        self.assertEqual(0.5, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, GREATER_THAN_HYPOTHESIS, x, mu=0.5))
        self.assertEqual(0.5, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, LESS_THAN_HYPOTHESIS, x, mu=0.5))
        self.assertEqual(0.0, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, TWO_SIDED_HYPOTHESIS, x, mu=0.0))
        self.assertEqual(1.0, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, GREATER_THAN_HYPOTHESIS, x, mu=0.0))
        self.assertEqual(0.0, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, LESS_THAN_HYPOTHESIS, x, mu=0.0))
        self.assertEqual(0.0, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, TWO_SIDED_HYPOTHESIS, x, mu=1.0))
        self.assertEqual(0.0, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, GREATER_THAN_HYPOTHESIS, x, mu=1.0))
        self.assertEqual(1.0, test(fakeStatistic, TWO_SIDED_HYPOTHESIS, LESS_THAN_HYPOTHESIS, x, mu=1.0))

    def testTransformSymmetricPValueHypothesis_NoOp(self):
        transform = transformSymmetricPValueHypothesis
        expected = 0.61
        self.assertEqual(expected, transform(0, 0.61, TWO_SIDED_HYPOTHESIS, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(expected, transform(0, 0.61, GREATER_THAN_HYPOTHESIS, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(expected, transform(0, 0.61, LESS_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS))

    def testTransformSymmetricPValueHypothesis_ToTwoSided(self):
        transform = transformSymmetricPValueHypothesis
        val = 0.41
        expected = min(val, 1-val)*2.0
        self.assertEqual(expected, transform(0, val, GREATER_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(expected, transform(0, val, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(expected, transform(-1, val, GREATER_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(expected, transform(-1, val, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(expected, transform(1, val, GREATER_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS))
        self.assertEqual(expected, transform(1, val, LESS_THAN_HYPOTHESIS, TWO_SIDED_HYPOTHESIS))

    def testTransformSymmetricPValueHypothesis_ToOneSided(self):
        transform = transformSymmetricPValueHypothesis
        val = 0.61
        self.assertEqual(val/2.0, transform(0, val, TWO_SIDED_HYPOTHESIS, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(val/2.0, transform(0, val, TWO_SIDED_HYPOTHESIS, LESS_THAN_HYPOTHESIS))
        self.assertEqual(val/2.0, transform(-1, val, TWO_SIDED_HYPOTHESIS, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(1-val/2.0, transform(-1, val, TWO_SIDED_HYPOTHESIS, LESS_THAN_HYPOTHESIS))
        self.assertEqual(1-val/2.0, transform(1, val, TWO_SIDED_HYPOTHESIS, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(val/2.0, transform(1, val, TWO_SIDED_HYPOTHESIS, LESS_THAN_HYPOTHESIS))

    def testTransformSymmetricPValueHypothesis_BetweenOneSided(self):
        transform = transformSymmetricPValueHypothesis
        val = 0.61
        self.assertEqual(1-val, transform(0, val, LESS_THAN_HYPOTHESIS, GREATER_THAN_HYPOTHESIS))
        self.assertEqual(1-val, transform(0, val, GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS))


def fakeStatistic(series, series2=None, mu=0.5):
    x = float(sum(series))/len(series)
    if series2:
        y = float(sum(series2))/len(series2)
    else:
        y = mu
    rawStat = 1.0 - 2.0*abs(x-y)
    score = (x-y)
    return score, max(0.0, min(1.0, rawStat))


if __name__ == "__main__":
    unittest.main()
