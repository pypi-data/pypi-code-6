"""
Main module for inversion counting, hypothesis tests, and
sequence transformations.  The exposed API of the package
relies on the implementations contained in this module.

Author: Benjamin D. Nye
License: Apache License V2.0
"""
from itertools import groupby
from InversionTest.InversionDistribution import (maxInversions, varianceOfInversions,
    similarityByInversions, correlationByInversions, rawInversionCounts)
from InversionTest.PolynomialOperations import polynomialExpansion, syntheticDivision
from InversionTest.StatisticalTests import (normalCDFFunction, signTest, wilcoxonSignedRankTest,
    permutationMeanTest, permutationRankTest, GREATER_THAN_HYPOTHESIS)


# Error Classes
class InvalidGradedPosetError(IndexError): pass
class MissingElementError(IndexError): pass

# Types of CDF Calculations and Measures
EXACT_CDF = 'exact'
NORMAL_CDF = 'normal'
ADAPTIVE_CDF = 'adaptive'
SIMILARITY_METRIC = 'similarity'
CDF_TYPES = frozenset([EXACT_CDF, NORMAL_CDF, ADAPTIVE_CDF])

# Types of Default Grades
LEFT_GRADE = 'Left'
ZERO_GRADE = 'Zero'
MEAN_GRADE = 'Mean'
MAX_GRADE  = 'Max'
RIGHT_GRADE = 'Right'
DEFAULT_GRADES = frozenset([LEFT_GRADE, ZERO_GRADE, MEAN_GRADE, MAX_GRADE, RIGHT_GRADE])

VALID_GRADE_CONTAINERS = (list, tuple, set)

class GradedPosetSequence(object):
    """
    An analysis of the inversion distribution of a graded poset
    This can be used to analyze the reference sequence against
    a sorted version of itself or against permutations of these
    elements in a sequence passed in (which may be graded or not).
    Note: When comparing two sequences, it should be noted that
    these inversion measures are symmetric with respect to which
    sequence is considered the reference versus the comparison.

    Graded sequences are represented through nested lists, where
    each subsequence contains the elements of a grade.  So then,
    the sequence: [[A,B,C], [1,2,3], [X,Y]] contains three grades,
    where A, B, and C have rank 1, [1,2,3] have rank 2, etc.  Elements
    that share a grade cannot have inversions between them.  The
    elements can be any valid Python objects that have valid comparison
    operations (including custom class instance).  However, if any
    of the elements cannot be hashed, the hashableElements flag must
    be set false or problems will occur.

    Note: Technically, while this code refers to ``permutations'', two
    sequences with the same elements but different grade structures
    are not technically permutations (though two with the same grade
    structure, regardless of structure, are certainly permutations).
    However, they are VERY close to permutations and may be considered
    analogous to permutations where you can't see the order of certain
    elements (i.e., censored observations).
    """
    # Approximation Bound - N to use approximations for an adaptive calculation
    APPROXIMATION_RANKS_BOUND = 100

    def __init__(self, sequence, isGraded=False, hashableElements=True, validate=False, defaultGrade=None):
        """
        Initialize the reference sequence
        @param sequence: Reference sequence, for comparing permutations against
        @type sequence: list of object or list of list of object
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @param hashableElements: If True, elements can be hashed (allowing slightly faster performance)
        @type hashableElements: bool
        @param validate: If True, run basic validation on the sequence inside
        @type validate: bool
        """
        self._sequence = sequence
        self._isGraded = isGraded
        self._hashableElements = hashableElements
        if validate:
            self.validate()
        self._sortedRanks = False
        self._hashRanks = None
        self._numElements = self._calcNumElements(self._sequence, self._isGraded)
        self._overloadedRanks = None
        self._defaultGrade = defaultGrade

    def __len__(self):
        """
        Get the number of grades in the sequence
        @return: Number of grades
        @rtype: int
        """
        return len(self._sequence)

    def __iter__(self):
        """
        Iterate over the grades/elements
        @return: If nested, yield a grade (and all elements in it).  If flat, yield an element.
        @rtype: list of object or object
        """
        for x in self._sequence:
            yield x

    def iterElements(self):
        """
        Iterate over the elements (flat iteration over grades)
        @return: Yield all the elements in the poset
        @rtype: list of object or object
        """
        if self._isGraded:
            for grade in self._sequence:
                if isinstance(grade, VALID_GRADE_CONTAINERS):
                    for x in grade:
                        yield x
                else:
                    yield grade
        else:
            for x in self._sequence:
                yield x

    def isGraded(self):
        """
        Return if this is a graded poset.  If True, is graded.
        """
        return self._isGraded

    def getNumElements(self):
        """
        Get the number of elements in this sequence
        @return: Number of elements
        @rtype: int
        """
        return self._numElements

    def getOverloadedRanks(self):
        """
        Get the elements in grades with more than one element
        @return: List of grades with their elements
        @rtype: list of list of object
        """
        if self._overloadedRanks is None:
            self._overloadedRanks = self._calcOverloadedRanks(self._sequence, self._isGraded)
        return self._overloadedRanks
        
    def maxInversions(self, sequence=None, isGraded=False):
        """
        The maximum possible inversions, given the number of elements and
        the number sharing each grade (e.g. ties).  If sequence param is
        given, the structure of the comparison sequence is considered also.
        @param sequence: Comparison sequence
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: Maximum possible number of inversions
        @rtype: int
        """
        return self._calcGradedStatistic(maxInversions, sequence, isGraded)
    
    def mean(self, sequence=None, isGraded=False):
        """
        The mean of inversion across permutations, given the number of elements
        and the number sharing each grade (e.g. ties).  If sequence param is
        given, the structure of the comparison sequence is considered also.
        @param sequence: Comparison sequence
        @type sequence: list of list of object or list of object  or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: Mean number of inversions across possible permutations
        @rtype: int
        """
        return self.maxInversions(sequence, isGraded)/2.0
        
    def variance(self, sequence=None, isGraded=False):
        """
        The variance of inversions across permutations, given the number of elements
        and the number sharing each grade (e.g. ties).  If sequence param is
        given, the structure of the comparison sequence is considered also.
        @param sequence: Comparison sequence
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: Variance of inversions across possible permutations
        @rtype: int
        """
        return self._calcGradedStatistic(varianceOfInversions, sequence, isGraded)

    def stdDev(self, sequence=None, isGraded=False):
        """
        The standard deviation of inversions across permutations, given the elements
        and the number sharing each grade (e.g. ties).  If sequence param is not
        given, the structure of the comparison sequence is considered also.
        @param sequence: Comparison sequence
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: Standard deviation of inversions across possible permutations
        @rtype: int
        """
        return self.variance(sequence, isGraded)**0.5
    
    def inversions(self, sequence=None, isGraded=False):
        """
        The inversions between the reference sequence and the comparison sequence.
        If the 'sequence' param is None, the comparison sequence is a fully sorted
        form of the reference sequence.
        @param sequence: Comparison sequence (If None, equivalent to a sorted reference sequence)
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: If 'sequence' given, number of inversions to turn it into reference sequence.
                 Else, the number of inversions to sort the reference sequence.
        @rtype: int
        """
        if sequence:
            if isinstance(sequence, GradedPosetSequence):
                isGraded = sequence.isGraded()
                sequence = sequence._sequence
            if self._hashableElements:
                if self._hashRanks is None:
                    self._populateHashRanks()
                indexSeq = makeFlatIndexSequence(sequence, self._sequence, isGraded, self._isGraded,
                                                 indexFunction=self._getElementIndex)
            else:
                indexSeq = makeFlatIndexSequence(sequence, self._sequence, isGraded, self._isGraded)
            return mergeSortInversionCount(indexSeq)[0]
        else:
            if self._isGraded:
                if not self._sortedRanks:
                    for i, grade in enumerate(self._sequence):
                        if isinstance(grade, list):
                            grade.sort()
                        elif isinstance(grade, VALID_GRADE_CONTAINERS):
                            self._sequence[i] = sorted(grade)
                    self._sortedRanks = True
                return mergeSortInversionCount([element for element in self.iterElements()])[0]
            else:
                return mergeSortInversionCount(self._sequence)[0]

    def similarity(self, sequence=None, isGraded=False):
        """
        The similarity of the reference sequence to a comparison sequence.  If the
        'sequence' param is None, the comparison sequence is a fully sorted form
        of the reference sequence.
        @param sequence: Comparison sequence (If None, equivalent to a sorted reference sequence)
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: The similarity of the reference sequence to the comparison sequence, in [0,1]
        @rtype: float
        """
        inversions = self.inversions(sequence, isGraded)
        maxInversions = self.maxInversions(sequence, isGraded)
        return similarityByInversions(inversions, maxInversions)

    def correlation(self, sequence=None, isGraded=False):
        """
        The correlation of the reference sequence to a comparison sequence.  If the
        'sequence' param is None, the comparison sequence is a fully sorted form
        of the reference sequence.  This is just a rescaled form of similarity.
        This should also be equivalent to a Kendall's Tau correlation under
        standard conditions.
        @param sequence: Comparison sequence (If None, equivalent to a sorted reference sequence)
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: The correlation of the reference sequence to the comparison sequence, in [-1,1]
        @rtype: float
        """
        inversions = self.inversions(sequence, isGraded)
        maxInversions = self.maxInversions(sequence, isGraded)
        return correlationByInversions(inversions, maxInversions)
    
    def cdf(self, sequence=None, isGraded=False, cdfType=ADAPTIVE_CDF):
        """
        Calculate a CDF value for inversions between the reference sequence
        abd a comparison sequence.  If the 'sequence' param is None, the comparison
        sequence is a fully sorted form of the reference sequence.  This can
        use either an exact distribution or a normal approximation.
        @param sequence: Comparison sequence (If None, equivalent to a sorted reference sequence)
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @param cdfType: The CDF function to use.  If ADAPTIVE_CDF, automatically switches to a normal
                        approximation when the # of elements exceeds a bound.  If EXACT_CDF,
                        calculates the PDF exactly and sums over it.  This gets slow and is
                        seldom necessary after about 100 elements.  If NORMAL_CDF, uses the
                        mean and variance to generate a normal distribution.  Except for
                        small numbers of elements or very large grades, this is advised.
        @type cdfType: str
        @return: P(x<=X) where x is a random variable for permutation inversions and X is
                 the number of inversions between the reference and comparison sequences.
        @rtype: float
        """
        if cdfType == NORMAL_CDF:
            return self.normalCDF(sequence, isGraded)
        elif cdfType == EXACT_CDF:
            return self.exactCDF(sequence, isGraded)
        else:
            maxInversions = self.maxInversions(sequence, isGraded)
            if maxInversions >= self.APPROXIMATION_RANKS_BOUND:
                return self.normalCDF(sequence, isGraded)
            else:
                return self.exactCDF(sequence, isGraded)
                
    def exactCDF(self, sequence=None, isGraded=False):
        """
        Calculate an exact CDF value for inversions between the reference sequence
        abd a comparison sequence.  If the 'sequence' param is None, the comparison
        sequence is a fully sorted form of the reference sequence.
        Note: The exact CDF calculation works very slowly as N gets greater than 100 elements.
        @param sequence: Comparison sequence (If None, equivalent to a sorted reference sequence)
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: P(x<=X) where x is a random variable for permutation inversions and X is
                 the number of inversions between the reference and comparison sequences.
        @rtype: float
        """
        inversions = self.inversions(sequence, isGraded)
        maxInversions = self.maxInversions(sequence, isGraded)
        # Special Invariant-Point Cases
        if maxInversions == 0:
            return None
        elif inversions == maxInversions:
            return 1.0
        # General Case
        else:
            if sequence:
                if isinstance(sequence, GradedPosetSequence):
                    isGraded = sequence.isGraded()
                    otherNumElements = sequence.getNumElements()
                    otherOverloadedRanks = sequence.getOverloadedRanks()
                    sequence = sequence._sequence
                else:
                    otherNumElements = self._calcNumElements(sequence, isGraded)
                    otherOverloadedRanks = self._calcOverloadedRanks(sequence, isGraded)
                # If sets of unequal size, discard extra elements from reference set to fit
                if otherNumElements != self._numElements:
                    overloadedRanks = self._calcOverloadedRanks(self._sequence, self._isGraded, sequence, isGraded)
                else:
                    overloadedRanks = self.getOverloadedRanks()
                intersectingRanks = self._calcRankIntersections(overloadedRanks, otherOverloadedRanks)
                numElements = otherNumElements
            else:
                overloadedRanks = self.getOverloadedRanks()
                otherOverloadedRanks = []
                intersectingRanks = []
                numElements = self.getNumElements()
            inversionDistribution = rawInversionCounts(numElements)
            for intersections in intersectingRanks:
                intersectionDistr = rawInversionCounts(len(intersections))
                inversionDistribution = polynomialExpansion(inversionDistribution, intersectionDistr)
            for overloadedRank in overloadedRanks + otherOverloadedRanks:
                overloadedDistr = rawInversionCounts(len(overloadedRank))
                inversionDistribution, remainder = syntheticDivision(inversionDistribution, overloadedDistr)
            # Sum over the smaller tail
            if inversions > maxInversions/2.0:
                return 1.0-float(sum(inversionDistribution[inversions+1:]))/sum(inversionDistribution)
            else:
                return float(sum(inversionDistribution[:inversions+1]))/sum(inversionDistribution)
       
    def normalCDF(self, sequence=None, isGraded=False):
        """
        Calculate an approximate CDF value for inversions between the reference sequence
        abd a comparison sequence.  If the 'sequence' param is None, the comparison
        sequence is a fully sorted form of the reference sequence.
        Note: The normal distribution gets quite accurate by N > 20 and should be used for larger
        sequences.
        @param sequence: Comparison sequence (If None, equivalent to a sorted reference sequence)
        @type sequence: list of list of object or list of object or None
        @param isGraded: If true, sequence consists of subsequences containing each grade.  Else, flat list.
        @type isGraded: bool
        @return: P(x<=X) where x is a random variable for permutation inversions and X is
                 the number of inversions between the reference and comparison sequences.
        @rtype: float
        """
        mean = self.mean(sequence, isGraded)
        stdDev = self.stdDev(sequence, isGraded)
        inversions = self.inversions(sequence, isGraded)
        if mean == 0:
            return None
        else:
            return normalCDFFunction(inversions, mean, stdDev)

    def signTest(self, sequences, sequences2=None, isGraded=False, measure=SIMILARITY_METRIC,
                 mu=0.5, alternative=GREATER_THAN_HYPOTHESIS):
        """
        Perform a Sign test on either the similarity or the complements of the CDF values,
        which are a measure of the match between the each sequence and the reference seq.
        This has the advantage of calculating based on the similarity, which is quicker than
        calculating the CDF probability of a particular inversion counts.  If two sequences
        are provided, this performs a two sample paired test.
        @param sequences: Multiple sequences that are permutations of the elements of this sequence
        @type sequences: list of list of object or list of list of list of object
        @param sequences2: Multiple sequences that are permutations (second sample)
        @type sequences2: list of list of object or list of list of list of object
        @param isGraded: If True, each sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @param measure: The measure to calculate for each sequence, either SIMILARITY_METRIC or from CDF_TYPES set
        @type measure: str
        @param mu: Assumed mean of the sign test, to allow assymetric testing
        @type mu: float
        @param alternative: Alternate hypothesis for the test, from StatisticalTests.TEST_HYPOTHESES set
        @type alternative: str
        @return: Probability of the null hypothesis
        @rtype: float
        """
        if mu >= 1 or mu <= 0:
            raise ValueError("Sign test mu should be in [0,1] but got: %s"%mu)
        return self._comparisonTest(signTest, sequences, sequences2, isGraded, measure, mu=mu, alternative=alternative)
        
    def wilcoxonTest(self, sequences, sequences2=None, isGraded=False, cdfType=ADAPTIVE_CDF,
                     alternative=GREATER_THAN_HYPOTHESIS):
        """
        Perform a Wilcoxon Rank Sum test on the complements of the CDF values,
        which are a measure of the match between the each sequence and the reference seq
        Mu cannot be set on this test, as it would violate the assumption of symmetry.
        If two sequences are provided, this performs a two-sample paired test.
        @param sequences: Multiple sequences that are permutations of the elements of this sequence
        @type sequences: list of list of object or list of list of list of object
        @param sequences2: Multiple sequences that are permutations (second sample)
        @type sequences2: list of list of object or list of list of list of object
        @param isGraded: If True, each sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @param cdfType: The type of CDF to calculate for the inversion counts, from CDF_TYPES set
        @type cdfType: str
        @param alternative: Alternative hypothesis for the test, from StatisticalTests.TEST_HYPOTHESES set
        @type alternative: str
        @return: Probability of the null hypothesis
        @rtype: float
        """
        if cdfType not in CDF_TYPES:
            raise TypeError("Wilcoxon Test received invalid CDF Type.  Must be one of: %s"%(CDF_TYPES,))
        if sequences2 is None:
            return self._comparisonTest(wilcoxonSignedRankTest, sequences, sequences2, isGraded,
                                        cdfType, mu=0.5, alternative=alternative)
        else:
            return self._comparisonTest(wilcoxonSignedRankTest, sequences, sequences2, isGraded,
                                        cdfType, alternative=alternative)

    def permutationMeanTest(self, sequences, sequences2, isGraded=False, measure=ADAPTIVE_CDF,
                            alternative=GREATER_THAN_HYPOTHESIS, pValue=0.95, iterations=100000,
                            useStoppingRule=True, maxExactN=7):
        """
        Perform a Permutation or Monte Carlo Mean Difference test on some measure
        (similarity or 1-CDF) for the match between the each sequence and the reference seq.
        This requires two samples, as these are shuffled to form the permutations.
        @param sequences: Multiple sequences that are permutations of the elements of this sequence
        @type sequences: list of list of object or list of list of list of object
        @param sequences2: Multiple sequences that are permutations (second sample)
        @type sequences2: list of list of object or list of list of list of object
        @param isGraded: If True, each sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @param measure: The type of CDF to calculate for the inversion counts, from CDF_TYPES set
        @type measure: str
        @param alternative: Alternative hypothesis for the test, from StatisticalTests.TEST_HYPOTHESES set
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
        @return: Probability of the null hypothesis
        @rtype: float
        """
        return self._comparisonTest(permutationMeanTest, sequences, sequences2, isGraded, measure,
                                    alternative=alternative, pValue=pValue, iterations=iterations,
                                    maxExactN=maxExactN)

    def permutationRankTest(self, sequences, sequences2, isGraded=False, measure=ADAPTIVE_CDF,
                            alternative=GREATER_THAN_HYPOTHESIS, pValue=0.95, iterations=100000,
                            useStoppingRule=True, maxExactN=7):
        """
        Perform a Permutation or Monte Carlo rank test on a measure (similarity or
        1-CDF) for the match between the each sequence and the reference seq.
        This requires two samples, as these are shuffled to form the permutations.
        @param sequences: Multiple sequences that are permutations of the elements of this sequence
        @type sequences: list of list of object or list of list of list of object
        @param sequences2: Multiple sequences that are permutations (second sample)
        @type sequences2: list of list of object or list of list of list of object
        @param isGraded: If True, each sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @param measure: The type of CDF to calculate for the inversion counts, from CDF_TYPES set
        @type measure: str
        @param alternative: Alternative hypothesis for the test, from StatisticalTests.TEST_HYPOTHESES set
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
        @return: Probability of the null hypothesis
        @rtype: float
        """
        return self._comparisonTest(permutationRankTest, sequences, sequences2, isGraded, measure,
                                    alternative=alternative, pValue=pValue, iterations=iterations,
                                    maxExactN=maxExactN)
    
    def _comparisonTest(self, test, sequences, sequences2=None, isGraded=False, measure=SIMILARITY_METRIC, **kwds):
        """
        Perform a hypothesis test on either the similarity or the complements of the CDF values,
        which are a measure of the match between the each sequence and the reference seq.
        If two sequences are provided, this performs a two sample test of an appropriate type.
        @param test: The hypothesis test function, in the form: f(sample1, sample1=None, **kwds)
        @type test: callable
        @param sequences: Multiple sequences that are permutations of the elements of this sequence
        @type sequences: list of list of object or list of list of list of object
        @param sequences2: Multiple sequences that are permutations (second sample)
        @type sequences2: list of list of object or list of list of list of object
        @param isGraded: If True, each sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @param measure: The measure to calculate for each sequence, either SIMILARITY_METRIC or from CDF_TYPES set
        @type measure: str
        @param kwds: Additional test-specific parameters passed to the test
        @type kwds: dict
        @return: Probability of the null hypothesis
        @rtype: float
        """
        if measure == SIMILARITY_METRIC:
            values = [self.similarity(seq, isGraded) for seq in sequences]
        else:
            values = [1.0-self.cdf(seq, isGraded, measure) for seq in sequences]
        if sequences2 is None:
            return test(values, **kwds)
        else:
            if measure == SIMILARITY_METRIC:
                values2 = [self.similarity(seq, isGraded) for seq in sequences2]
            else:
                values2 = [1.0-self.cdf(seq, isGraded, measure) for seq in sequences2]
            return test(values, values2, **kwds)

    @classmethod
    def _calcNumElements(cls, sequence, isGraded):
        """
        Calculate the number of elements in the sequence.
        This is trivial for a flat sequence and quick for a graded one.
        @param sequence: The sequence to count elements in
        @type sequence: list of list of object or list of object
        @param isGraded: If True, sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @return: The number of elements in the sequence (N)
        @rtype: bool
        """
        if isGraded:
            aSum = 0
            for elements in sequence:
                if isinstance(elements, VALID_GRADE_CONTAINERS):
                    aSum += len(elements)
                else:
                    aSum += 1
            return aSum
        else:
            return len(sequence)

    def _calcGradedStatistic(self, operation, sequence=None, isGraded=False):
        """
        Calculate a series length statistic, adjusting for incomparable elements.
        This assumes that the operation can be evaluated on the total number of elements,
        then the operation is evaluated on the subsets of incomparable elements, which
        are subtracted off from the full-set operation value.  If the 'sequence' param is
        provided, the grades for this sequence is subtracted off also (without double-counting).
        The max, mean, and variance can all be calculated using this approach.
        @param operation: The operation to evaluate, in the form 'numeric = f(int)'
        @type operation: callable
        @param sequence: A comparison sequence to evaluate grades for also.  If None, ignored.
        @type sequence: list of list of object or list of object
        @param isGraded: If True, sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @return: Value of the graded statistic
        @rtype: int or float
        """
        if sequence:
            if isinstance(sequence, GradedPosetSequence):
                isGraded = sequence.isGraded()
                otherNumElements = sequence.getNumElements()
                otherOverloadedRanks = sequence.getOverloadedRanks()
                sequence = sequence._sequence
            else:    
                otherNumElements = self._calcNumElements(sequence, isGraded)
                otherOverloadedRanks = self._calcOverloadedRanks(sequence, isGraded)
            # If sets of unequal size, discard extra elements from reference set to fit
            if otherNumElements != self._numElements:
                overloadedRanks = self._calcOverloadedRanks(self._sequence, self._isGraded, sequence, isGraded)
            else:
                overloadedRanks = self.getOverloadedRanks()
            intersectingRanks = self._calcRankIntersections(overloadedRanks, otherOverloadedRanks)
            value = operation(min(otherNumElements, self._numElements))
            value -= sum([operation(len(elements)) for elements in overloadedRanks])
            value -= sum([operation(len(elements)) for elements in otherOverloadedRanks])
            value += sum([operation(len(elements)) for elements in intersectingRanks])
            return value
        else:
            value = operation(self._numElements)
            value -= sum([operation(len(elements)) for elements in self.getOverloadedRanks()])
            return value
        
    def _calcOverloadedRanks(self, sequence, isGraded, otherSequence=None, isOtherGraded=False):
        """
        Calculate the grades with more than one element (overloaded grades).
        If two sequences are provided, this only calculates overloaded ranks for elements
        that are contained in both sequences (in case one is missing elements)
        Note: If a sequence is not nested, it has no overloaded ranks by definition
        Note 2: The 'otherSequence' is only needed to handle missing elements 
        @param sequence: Sequence to calculate the overloaded grades
        @type sequence: list of list of object or list of object
        @param isGraded: If True, sequence is nested (where nested elements share a grade)
        @type isGraded: bool
        @param otherSequence: Optionally, a reference sequence to only count elements in both sequences
        @type otherSequence: list of list of object or list of object
        @param isOtherGraded: If True, sequence is nested (where nested elements share a grade)
        @type isOtherGraded: bool
        @return: List of subsets of elements that cannot be compared against each other
        @rtype: List of list of object
        """
        if isinstance(sequence, GradedPosetSequence):
            isGraded = sequence.isGraded()
            sequence = sequence._sequence
        if otherSequence and isinstance(otherSequence, GradedPosetSequence):
            isOtherGraded = otherSequence.isGraded()
            otherSequence = otherSequence._sequence
        if isGraded:
            if otherSequence is None:
                overloadedRanks = [elements for elements in sequence
                                   if isinstance(elements, VALID_GRADE_CONTAINERS)
                                   and len(elements) > 1]
            else:
                # Flatten a nested other sequence
                if isOtherGraded:
                    if self._hashableElements:
                        flatOther = set()
                        for elements in otherSequence:
                            if isinstance(elements, VALID_GRADE_CONTAINERS):
                                flatOther |= set(elements)
                            else:
                                flatOther.add(elements)
                    else:
                        flatOther = []
                        for elements in otherSequence:
                            if isinstance(elements, VALID_GRADE_CONTAINERS):
                                flatOther.extend(elements)
                            else:
                                flatOther.append(elements)
                else:
                    if self._hashableElements:
                        flatOther = set(otherSequence)
                    else:
                        flatOther = otherSequence
                # Find overloaded ranks that contain only elements from the other sequence
                overloadedRanks = []
                for elements in sequence:
                    if isinstance(elements, VALID_GRADE_CONTAINERS) and len(elements) > 1:
                        filteredElements = [element for element in elements if element in flatOther]
                        if len(filteredElements) > 1:
                            overloadedRanks.append(filteredElements)
        else:
            overloadedRanks = []
        return overloadedRanks

    def _calcRankIntersections(self, overloadedRanks, overloadedRanks2):
        """
        Calculate the intersection of overloaded ranks between sequences.
        This basically calculates "overloaded overloads" of ranks.
        @param overloadedRanks: First set of overloaded (len > 1) ranks
        @type overloadedRanks: list of list of object
        param overloadedRanks2: Second set of overloaded (len > 1) ranks
        @type overloadedRanks2: list of list of object
        @return: List of intersections between overloaded grades
        @rtype: list of list of object
        """
        intersections = []
        if self._hashableElements:
            intersections= [list(set.intersection(set(elements1), set(elements2)))
                            for elements1 in overloadedRanks
                            for elements2 in overloadedRanks2]
        else:
            intersections= [filter(lambda x: x in elements1, elements2)
                            for elements1 in overloadedRanks
                            for elements2 in overloadedRanks2]
        intersections = [x for x in intersections if len(x) > 1]
        return intersections

    def _populateHashRanks(self):
        """
        Populate hash table that reports the grade of any element.
        Slight hit to memory, but significant boost in speed for
        comparisons.
        """
        sequence = self._sequence
        if self._isGraded:
            self._hashRanks = {}
            for i, elements in enumerate(sequence):
                if isinstance(elements, VALID_GRADE_CONTAINERS):
                    for e in elements:
                        self._hashRanks[e] = i
                else:
                    self._hashRanks[elements] = i
        else:
            self._hashRanks = dict(((x,i) for i, x in enumerate(sequence)))

    def _getElementIndex(self, element, sequence, isGraded=False):
        """
        Get the index of the given value in the sequence
        Note: This hashes element indices, if possible
        @param element: Value to get the position for
        @type element: object
        @param sequence: Nested sequence which is used to determine sorting value of elements
        @type sequence: list of list of object
        @param isGraded: If True, sequence is graded (nested).  Else, flat sequence.
        @type isGraded: bool
        @return: Sorting key for the value
        @rtype: int
        """
        if self._hashableElements:
            value = self._hashRanks.get(element, None)
            if value is not None:
                return value
            else:
                return getDefaultIndex(element, len(self._sequence), self._defaultGrade)
        else:
            return getValueIndex(element, sequence, isGraded)

    
    def validate(self):
        """
        Check that this sequence is valid, so that it has
        no repeated elements, that elements are hashable
        if sequence is hashable, and that a graded sequence
        contains iterated grades.
        """
        self.validateSequence(self._sequence, self._isGraded, self._hashableElements)

    @classmethod
    def validateSequence(cls, sequence, isGraded=False, hashableElements=True):
        """
        Check that a sequence is valid, so that it has
        no repeated elements, and that elements are hashable
        if sequence is hashable.
        """
        if hasattr(sequence, '__iter__'):
            if isGraded:
                elements = []
                for grade in sequence:
                    if isinstance(grade, VALID_GRADE_CONTAINERS):
                        elements.extend(grade)
                    else:
                        elements.append(grade)
            else:
                elements = list(sequence)
            # Collect the unhashables
            if hashableElements:
                unhashables = []
                for element in elements:
                    if not hasattr(element, '__hash__') or element.__hash__ is None:
                        unhashables.append(element)
                    else:
                        hash(element)
            # Collect repeated elements
            observedElements = []
            repeatedElements = []
            for element in elements:
                if element in observedElements:
                    repeatedElements.append(element)
                else:
                    observedElements.append(element)
            errStr = ''
            if len(unhashables) > 0:
                unhashableStr = ', '.join([str(unhashable) for unhashable in unhashables])
                errStr +="The following elements were unhashable in a hashable poset:\n%s\n"%(unhashableStr,)
            if len(repeatedElements) > 0:
                errStr += "The following elements were repeated in the poset:\n%s"%(repeatedElements,)
        else:
            errStr = 'Sequence was not iterable.'
        if len(errStr) > 0:
            raise InvalidGradedPosetError(errStr)

###########################
#   Descriptive Measures  #
###########################

def inversionCountMax(seq, seq2=None, isGraded=False, hashableElements=True):
    """
    Calculate the maximum possible number of inversions, based
    on the sequence (# of elements and grade structure).  If
    the second optional sequence is provided, its grade structure
    is also considered.
    Note: This only depends on the structure of the sequence(s), not their order
    @param seq: Sequence to get the maximum possible inversions for any permutation
    @type seq: list of object or list of list of object
    @param seq2: A comparison sequence for the sequence 'seq'
    @type seq2: list of object or list of list of object
    @param isGraded: If True, both seq and seq2 are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @return: Maximum inversions
    @rtype: int
    """
    if isinstance(seq, GradedPosetSequence):
        refSeq = seq
    else:
        refSeq = GradedPosetSequence(seq, isGraded=isGraded, hashableElements=hashableElements)
    return refSeq.maxInversions(seq2, isGraded)

def inversionCountMean(seq, seq2=None, isGraded=False, hashableElements=True):
    """
    Calculate the mean inversions across permutations, based
    on the sequence (# of elements and grade structure).  If
    the second optional sequence is provided, its grade structure
    is also considered.
    Note: This only depends on the structure of the sequence(s), not their order
    @param seq: Sequence to get the mean inversions for all possible permutations
    @type seq: list of object or list of list of object
    @param seq2: A comparison sequence for the sequence 'seq'
    @type seq2: list of object or list of list of object
    @param isGraded: If True, both seq and seq2 are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @return: Mean inversions
    @rtype: float
    """
    if isinstance(seq, GradedPosetSequence):
        refSeq = seq
    else:
        refSeq = GradedPosetSequence(seq, isGraded=isGraded, hashableElements=hashableElements)
    return refSeq.mean(seq2, isGraded)

def inversionCountVariance(seq, seq2=None, isGraded=False, hashableElements=True):
    """
    Calculate the variance of inversions across permutations, based
    on the sequence (# of elements and grade structure).  If
    the second optional sequence is provided, its grade structure
    is also considered.
    Note: This only depends on the structure of the sequence(s), not their order
    @param seq: Sequence to get the variance of inversions for all possible permutations
    @type seq: list of object or list of list of object
    @param seq2: A comparison sequence for the sequence 'seq'
    @type seq2: list of object or list of list of object
    @param isGraded: If True, both seq and seq2 are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @return: Variance of inversions
    @rtype: float
    """
    if isinstance(seq, GradedPosetSequence):
        refSeq = seq
    else:
        refSeq = GradedPosetSequence(seq, isGraded=isGraded, hashableElements=hashableElements)
    return refSeq.variance(seq2, isGraded)

def medianSequence(permutations, isGraded=False, hashableElements=True):
    """
    From the given permutations, make a sequence ordered by the median
    rank of each element.  Note: This requires that all permutations
    contain the same set of elements.  If this condition does not hold,
    then permutations with less elements would by definition have lower
    median ranks.  As such, this raises a KeyError if this case occurs.

    In addition to providing a view into the typical sequence from a set,
    the median sequence can also be used in combination with other functions.
    In particular,  the similarity of the median sequence can remove noise
    from outlier sequences.  If deviation of orderings from the comparison
    sequence occurs largely due to random noise, the median sequence should
    have a high similarity value.  Finally, the ordering derived from median
    ranks has been demonstrated to have an approximation factor of less than
    2 when analyzing orderings of elements (Fagin, 2004).
    
    @param permutations: Permutations to gather the ranks for
    @type permutations: list of list of object or list of list of list of object
    @param isGraded: If True, both seq and seq2 are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @return: A graded sequence based on the median ranks of elements.
             Grades occur if elements share the same median rank.
    @rtype: list of list of object
    """
    if len(permutations) == 0:
        return []
    # If Hashable, Collect Indices in a Dictionary and Get Median Indices
    if hashableElements:
        indices = {}
        for n, permutation in enumerate(permutations):
            for i, x in enumerate(permutation):
                if isGraded and isinstance(x, VALID_GRADE_CONTAINERS):
                    elements = x
                else:
                    elements = [x]
                for element in elements:
                    if n == 0:
                        indices[element] = []
                    indices[element].append(i)
        indices = [(getMedianValue(values), e) for e, values in indices.iteritems()]
    # Otherwise, Collect Indices in a Flat List, Sort, Collect, and Get Median Indices
    else:
        indices = []
        for permutation in permutations:
            for i, x in enumerate(permutation):
                if isGraded and isinstance(x, VALID_GRADE_CONTAINERS):
                    elements = x
                else:
                    elements = [x]
                for element in elements:
                    indices.append((element,i))
        indices.sort()
        newIndices = []
        for element, i in indices:
            if len(newIndices) == 0 or newIndices[-1][0] != element:
                newIndices.append((element, [i]))
            else:
                newIndices[-1][1].append(i)
        indices = [(getMedianValue(values), e) for e, values in newIndices]
    indices.sort()
    # Turn the list of indices into a graded sequence
    medianSeq = []
    lastIndex = None
    for indexVal, e in indices:
        if lastIndex is None or lastIndex != indexVal:
            medianSeq.append([e])
            lastIndex = indexVal
        else:
            medianSeq[-1].append(e)
    return medianSeq
        

####################
# Inversion Counts #
####################

def mergeSortInversionCount(sequence):
    """
    Calculate the number of inversions requried to sort sequence via mergesort.
    This function only works on a flat list.  
    Note: Relies on python sort to do actual merging (but not the counting).
    More efficient this way, as the Python version is in C.
    @param sequence: Sequence to sort and count inversions
    @type sequence: list
    @return: Number of inversions, sorted list
    @rtype: int, list
    """
    if len(sequence) <= 1:
        return 0, sequence
    else:
        firstHalf = sequence[:int(len(sequence)/2)]
        secondHalf = sequence[int(len(sequence)/2):]
        count1, firstHalf = mergeSortInversionCount(firstHalf)
        count2, secondHalf = mergeSortInversionCount(secondHalf)
        firstN = len(firstHalf)
        secondN = len(secondHalf)
        secondHalfEnd = secondN
        count3 = count1
        count3+= count2
        # Count the inversions in the merge
        # Uses a countdown through each sublist
        for i in xrange(firstN-1, -1, -1):
            x = firstHalf[i]
            inversionFound = False
            for j in xrange(secondHalfEnd-1,-1,-1):
                if x > secondHalf[j]:
                    inversionFound = True
                    break
            if inversionFound:
                secondHalfEnd = j+1
                count3 += j+1
        mergeList = firstHalf + secondHalf
        mergeList.sort()
        return count3, mergeList
    
def inversionCount(seq, seq2=None, isGraded=False, hashableElements=True):
    """
    Calculate the inversions between seq and seq2.  If seq2 is None, this works
    equivalently to seq2 being a sorted version of seq
    @param seq: Sequence to calculate the inversions for
    @type seq: list of object or list of list of object
    @param seq2: A comparison sequence for the sequence 'seq'
    @type seq2: list of object or list of list of object
    @param isGraded: If True, both seq and seq2 are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @return: Number of inversions
    @rtype: int
    """
    if isinstance(seq, GradedPosetSequence):
        refSeq = seq
    else:
        refSeq = GradedPosetSequence(seq, isGraded=isGraded, hashableElements=hashableElements)
    return refSeq.inversions(seq2, isGraded)

def inversionSimilarity(seq, seq2=None, isGraded=False, hashableElements=True):
    """
    Calculate the similarity between sequences: 1-inversions/maxInversions
    If seq2 is None, this works equivalently to seq2 being a sorted version of seq

    The inversionSimilarity function returns the complement of the actual number of
    inversions divided by the maximum possible number of inversions (1-inversions/maxInversion).
    If a comparison sequence is not provided, this uses the number of inversions to sort seq.
    To note, the similarity value is related to the tie-adjusted Kendall's Tau statistic
    as per: Kendall's tau = 2*inversionSimilarity-1. 
    
    @param seq: Sequence to get the similarity for
    @type seq: list of object or list of list of object
    @param seq2: A comparison sequence for the sequence 'seq'
    @type seq2: list of object or list of list of object
    @param isGraded: If True, both seq and seq2 are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @return: Similarity of sequences by inversion counts, in [0,1], where 1 is a perfect match
    @rtype: float
    """
    if isinstance(seq, GradedPosetSequence):
        refSeq = seq
    else:
        refSeq = GradedPosetSequence(seq, isGraded=isGraded, hashableElements=hashableElements)
    return refSeq.similarity(seq2, isGraded)


##################################
#   Probability and Statistics   #
##################################

def inversionCountCDF(seq, seq2=None, isGraded=False, hashableElements=True, cdfType=ADAPTIVE_CDF):
    """
    Get the cummulative distribution function probability for the number
    of inversions between seq and seq2.  If seq2 is None, this works
    equivalently to seq2 being a sorted version of seq
    @param seq: Sequence to calculate the number of inversions
    @type seq: list of object or list of list of object
    @param seq2: A comparison sequence for the sequence 'seq'
    @type seq2: list of object or list of list of object
    @param isGraded: If True, both seq and seq2 are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @return: P(X<=x) where X is a R.V. based on all permutations and
             x is the actual number of inversions between seq and seq2
    @rtype: float
    """
    if isinstance(seq, GradedPosetSequence):
        refSeq = seq
    else:
        refSeq = GradedPosetSequence(seq, isGraded=isGraded, hashableElements=hashableElements)
    return refSeq.cdf(seq2, isGraded, cdfType)


def inversionSignTest(orderings, orderings2=None, seq=None, isGraded=False, hashableElements=True,
                      measure=SIMILARITY_METRIC, alternative=GREATER_THAN_HYPOTHESIS, mu=0.5):
    """
    A sign test based on the values of some measure.  This measure can be either similarity
    or the complement of the cdf (1-cdf), both of which are in the range [0,1] where
    0 is the worst match and 1 is the best match.  For each sequence in 'orderings',
    the measure is calculated comparing seq against the permutation.  This creates a list
    of measure values that the sign test can be applied to.  If two sets of orderings
    are provided, this runs a two-sample test and ignores mu.

    To note, the inversionSignTest works slightly differently than the inversionWilcoxonTest.
    An additional parameter, mu, allows this test to set the value that the test is
    centered around.  A sign test examines the binomial distribution of values greater than
    mu (successes) and less than mu (failures).  So then, mu=0.5 would test would be centered
    around the expectation of purely random orderings, while mu=0.8 would set a much higher bar
    for similarity.  However, the measure parameter works slightly differently than the cdfType
    used by inversionWilcoxonTest.  In addition to taking any of the valid CDF types,
    the SIMILARITY_METRIC identifier is also a valid value.  This allows the sign test to use the
    similarity, rather than the more costly calculation of a CDF value.  When mu=0.5, these measures
    are entirely equivalent for the sign test.  However, for other values of mu, the similarity and
    complement of the CDF must be interpreted separately.  This test is also less powerful than
    the Wilcoxon signed-rank test under some conditions, but the sign test can be used to evaluate
    different central tendencies (which the Wilcoxon signed-rank test cannot evaluate because it
    requires symmetry around mu).
    
    Note: A calculation based on similarity will provide different results than one based
    on CDF if mu!=0.5.  When mu=0.5, both are identical.
    @param orderings: One or more comparison sequences (first sample)
    @type orderings: list of list of object or list of list of list of object
    @param orderings2: One or more comparison sequences (second sample)
    @type orderings2: list of list of object or list of list of list of object
    @param seq: Reference sequence to calculate the number of inversions against
    @type seq: list of object or list of list of object
    @param isGraded: If True, both 'seq' and sequences in 'orderings' are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @param measure: The measure to calculate for each sequence, either SIMILARITY_METRIC or from CDF_TYPES set
    @type measure: str
    @param mu: Assumed mean of the sign test, to allow assymetric testing
    @type mu: float
    @param alternative: Alternate hypothesis for the test, from the TEST_HYPOTHESES set ('greater', 'less', 'two.sided')
    @type alternative: str
    @return: Probability of the null hypothesis
    @rtype: float    
    """
    if mu >= 1 or mu <= 0:
        raise ValueError("Sign test mu should be in [0,1] but got: %s"%mu)
    return _inversionComparisonTest(signTest, GradedPosetSequence.signTest, orderings, orderings2, seq,
                                    isGraded, hashableElements, measure, mu=mu, alternative=alternative)


def inversionWilcoxonTest(orderings, orderings2=None, seq=None, isGraded=False, hashableElements=True,
                          cdfType=ADAPTIVE_CDF, alternative=GREATER_THAN_HYPOTHESIS):
    """
    A Wilcoxon rank sum test based on the complement of the CDF (1-cdf).
    For each ordering in 'orderings', 1-cdf is calculated comparing seq
    against the permutation.  This creates a list of probabilities of getting
    a worse match by chance (one probability for each comparison sequence).

    The inversionWilcoxonTest compares a sample of sequences (orderings) against a single sequence
    (seq).  This function applies a Wilcoxon signed-rank test based on the complement of the CDF (1-cdf).
    For each sequence in orderings, one minus the inversionCountCDF value for the pair is calculated
    comparing seq against the ordering.  If seq is not provided, the orderings are compared against
    their sorted forms.  This creates a list of probabilities of getting a worse match by chance
    (one such probability for each comparison sequence).  These probabilities are passed to a
    single-population Wilcoxon signed-rank test that compares them against a median (mu) of 0.5
    (the expected CDF value for a set of purely random permutations).  If a second set of orderings
    is provided, this calculates a two sample test instead.  The Wilcoxon signed-rank test is a
    non-parametric test to determine how the population medians differ (Wilcoxon, 1945).

    The cdfType follows the same convention as inversionCountCDF, which this function consumes.
    As this function provides a hypothesis test, the alternative parameter determines the
    alternate hypothesis for the Wilcoxon signed-rank test.  For this test, GREATER_THAN_HYPOTHESIS,
    LESS_THAN_HYPOTHESIS, and TWO_SIDED_HYPOTHESIS are possible constants.  The text equivalents of
    these hypotheses were chosen to match those used by R convention (``greater'', ``less'', and
    ``two.sided'').  For example, if \code{alternative} is ``greater'' then a return value of
    0.01 indicates that the orderings are much closer to seq than expected by chance.  Finally,
    it should be noted that this implementation of the Wilcoxon signed-rank test adjusts for each
    set of ties using a variance penalty of $(t^3-t)/48.0$ where t is the number of sequences sharing
    the same CDF value.  This is a standard method of adjusting the test statistic for ties, but
    is important to note because some interoperable packages (e.g., SciPy, 2001) do not always adjust
    for ties for these tests.  While this function does adjust for ties, users should note that
    the Wilcoxon signed-rank test is only useful when ties are infrequent.  Where many ties exist,
    more advanced tests such as permutation tests are recommended.
    
    @param orderings: One or more comparison sequences (first sample)
    @type orderings: list of list of object or list of list of list of object
    @param orderings2: One or more comparison sequences (second sample)
    @type orderings2: list of list of object or list of list of list of object
    @param seq: Sequence to calculate the number of inversions
    @type seq: list of object or list of list of object
    @param isGraded: If True, both 'seq' and sequences in 'orderings' are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @param cdfType: The type of CDF to calculate for the inversion counts, from CDF_TYPES set
    @type cdfType: str
    @param alternative: Alternate hypothesis for the test, from the TEST_HYPOTHESES set ('greater', 'less', 'two.sided')
    @type alternative: str
    @return: Probability of the null hypothesis
    @rtype: float    
    """
    if cdfType not in CDF_TYPES:
        raise TypeError("Wilcoxon Test received invalid CDF Type.  Must be one of: %s"%(CDF_TYPES,))
    if orderings2 is None and seq is None:
        return _inversionComparisonTest(wilcoxonSignedRankTest, GradedPosetSequence.wilcoxonTest,
                                        orderings, orderings2, seq, isGraded, hashableElements, cdfType,
                                        mu=0.5, alternative=alternative)
    else:
        return _inversionComparisonTest(wilcoxonSignedRankTest, GradedPosetSequence.wilcoxonTest,
                                        orderings, orderings2, seq, isGraded, hashableElements, cdfType,
                                        alternative=alternative)


def inversionPermutationMeanTest(orderings, orderings2, seq=None, isGraded=False, hashableElements=True,
                                 measure=ADAPTIVE_CDF, alternative=GREATER_THAN_HYPOTHESIS,
                                 pValue=0.95, iterations=100000, useStoppingRule=True, maxExactN=7):
    """
    Perform a Permutation or Monte Carlo Mean Difference Test on some measure
    (similarity or 1-CDF) for the match between the each sequence and the reference seq.
    This requires two samples, as these are shuffled to form the permutations.

    For this permutation test, each set of orderings is transformed to a set of values calculated
    using an inversion counting measure (e.g., similarity).  For each set of orderings, the mean
    value of the measure values is calculated.  The difference of these means is then calculated (i.e.,
    mean of measures from orderings2 - mean of measures from orderings).  This mean difference is the
    observed value.  An exact or approximate (Monte Carlo) permutation test is performed to determine
    the probability of the test hypothesis about this observed value.  For each permutation of the
    labels of the elements in orderings and orderings2, the difference between the means is
    recalculated and used to derive a distribution for calculating 

    Tests the total number of elements is small (no greater than maxExactN), an exact permutation test
    is used to calculate the probability.  For larger N, a Monte Carlo test is used to sample and
    approximate the full distribution.  The Monte Carlo test can be run for the full number of samples
    or can implement a stopping rule for higher efficiency.  When useStoppingRule is False, the Monte
    Carlo test samples the full number of samples given in the iterations parameter.  When
    useStoppingRule is True, the Monte Carlo sampler applies the MCB (Monte Carlo Bound) stopping rule
    described in Kim (2010).  This stopping rule treats iterations as the maximum number of samples
    and terminates when the distribution deviates significantly from the test pValue sufficiently to
    end the test with a positive or negative conclusion.  

    Use of the stopping rule is highly recommended, since it takes advantage of the power from setting
    much higher numbers of iterations while keeping the test computationally efficient.  However, one
    caveat is that while early stopping rules allow significantly higher power for evaluating the
    hypothesis and are unbiased with respect to testing the hypothesis, they may not give an unbiased
    estimate of the overall hypothesis probability.  This is because the test is likely to end before
    the estimate reaches tails beyond what are needed to confirm (or disconfirm) the hypothesis.
    
    @param orderings: One or more comparison sequences (first sample)
    @type orderings: list of list of object or list of list of list of object
    @param orderings2: One or more comparison sequences (second sample)
    @type orderings2: list of list of object or list of list of list of object
    @param seq: Sequence to calculate the number of inversions
    @type seq: list of object or list of list of object
    @param isGraded: If True, both 'seq' and sequences in 'orderings' are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @param measure: The type of CDF to calculate for the inversion counts, from CDF_TYPES set
    @type measure: str
    @param alternative: Alternative hypothesis for the test, from StatisticalTests.TEST_HYPOTHESES set
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
    @return: Probability of the null hypothesis
    @rtype: float
    """
    return _inversionComparisonTest(permutationMeanTest, GradedPosetSequence.permutationMeanTest,
                                    orderings, orderings2, seq, isGraded, hashableElements, measure,
                                    alternative=alternative, pValue=pValue, iterations=iterations,
                                    maxExactN=maxExactN)

def inversionPermutationRankTest(orderings, orderings2, seq=None, isGraded=False, hashableElements=True,
                                 measure=ADAPTIVE_CDF, alternative=GREATER_THAN_HYPOTHESIS,
                                 pValue=0.95, iterations=100000, useStoppingRule=True, maxExactN=7):
    """
    Perform a Permutation or Monte Carlo Rank on some measure (similarity or 1-CDF)
    for the match between the each sequence and the reference seq.
    This requires two samples, as these are shuffled to form the permutations.

    The inversionPermutationRankTest offers permutation or Monte Carlo style hypothesis
    testing similar to that done by inversionPermutationMeanTest, but using the
    distribution of rank sums, rather than mean differences.  This means that the raw
    measure values as used by the inversionPermutationMeanTest are first transformed
    into their rank values.  The rank sum of orderings2 is used as the observed value.
    The sampled distribution of this rank sum is then generated using full permutation
    or Monte Carlo sampling, to evaluate the test hypothesis.  This test is otherwise identical
    to the inversionPermutationMeanTest and all parameters have the same meaning and interpretation.
    The Python code for the Monte Carlo hypothesis testing code is also available in the package,
    which can be used by advanced users to implement  custom statistic functions other than mean
    difference or rank sum.

    @param orderings: One or more comparison sequences (first sample)
    @type orderings: list of list of object or list of list of list of object
    @param orderings2: One or more comparison sequences (second sample)
    @type orderings2: list of list of object or list of list of list of object
    @param seq: Sequence to calculate the number of inversions
    @type seq: list of object or list of list of object
    @param isGraded: If True, both 'seq' and sequences in 'orderings' are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @param measure: The type of CDF to calculate for the inversion counts, from CDF_TYPES set
    @type measure: str
    @param alternative: Alternative hypothesis for the test, from StatisticalTests.TEST_HYPOTHESES set
    @type alternative: str
    @param pValue: The p-Value for the test to confirm, used for Monte Carlo early termination
    @type pValue: float
    @param useStoppingRule: If True, use version of MonteCarlo with an unbiased early stopping rule
    @type useStoppingRule: bool    
    @param iterations: The max number of iterations to run for Monte Carlo
    @type iterations: int
    @param maxExactN: The largest N=len(x)+len(y) to calculate an exact test value.
                      For values higher than this, use a Monte Carlo approximation.
    @type maxExactN: int    
    @return: Probability of the null hypothesis
    @rtype: float
    """
    return _inversionComparisonTest(permutationRankTest, GradedPosetSequence.permutationRankTest,
                                    orderings, orderings2, seq, isGraded, hashableElements, measure,
                                    alternative=alternative, pValue=pValue, iterations=iterations,
                                    maxExactN=maxExactN)


def _inversionComparisonTest(test, classTest, orderings, orderings2=None, seq=None, isGraded=False,
                             hashableElements=True, measure=ADAPTIVE_CDF, **kwds):
    """
    A hypothesis test for comparing the similarity of some orderings based on some
    test function (test) and its equivalent in the GradedPosetSequence class (classTest).
    @param test: A test function, in the form, f(orderings, orderings2, **kwds)
    @type test: callable
    @param classTest: An unbound method for the GradedPosetSequence class, in the form
                      f(self, orderings, orderings2, isGraded, measure, **kwds)
    @type classTest: callable
    @param orderings: One or more comparison sequences (first sample)
    @type orderings: list of list of object or list of list of list of object
    @param orderings2: One or more comparison sequences (second sample)
    @type orderings2: list of list of object or list of list of list of object
    @param seq: Sequence to calculate the number of inversions
    @type seq: list of object or list of list of object
    @param isGraded: If True, both 'seq' and sequences in 'orderings' are nested (where nested elements share a grade)
    @type isGraded: bool
    @param hashableElements: If True, elements can be hashed (improves speed)
    @type hashableElements: bool
    @param measure: The type of CDF or similarity to calculate for the inversion counts
    @type measure: str
    @return: Probability of the null hypothesis
    @rtype: float    
    """
    if seq is None:
        f = lambda x: GradedPosetSequence(x, isGraded=isGraded, hashableElements=hashableElements)
        if measure == SIMILARITY_METRIC:
            mFunct = lambda x: x.similarity(isGraded=isGraded)
        else:
            mFunct = lambda x: 1.0-x.cdf(isGraded=isGraded, cdfType=measure)
        vals = [mFunct(f(x)) for x in orderings]
        if orderings2 is None:
            return test(vals, **kwds)
        else:
            vals2 = [mFunct(f(x)) for x in orderings2]
            return test(vals, vals2, **kwds)
    else:
        if isinstance(seq, GradedPosetSequence):
            refSeq = seq
        else:
            refSeq = GradedPosetSequence(seq, isGraded=isGraded, hashableElements=hashableElements)
        if classTest is None:
            return refSeq._comparisonTest(test, orderings, orderings2, isGraded, measure, **kwds)
        else:
            return classTest(refSeq, orderings, orderings2, isGraded, measure, **kwds)


def pairwiseGroupComparison(orderings, orderings2, isGraded=False, hashableElements=True,
                            cdfType=ADAPTIVE_CDF, alternative=GREATER_THAN_HYPOTHESIS):
    if measure == SIMILARITY_METRIC:
        mFunct = lambda x,y: x.similarity(y, isGraded=isGraded)
    else:
        mFunct = lambda x,y: 1.0-x.cdf(y, isGraded=isGraded, cdfType=measure)
    group1 = []
    crossGroup = []
    for i, x in enumerate(orderings):
        x = GradedPosetSequence(x, isGraded=isGraded, hashableElements=hashableElements)
        group1.extend([mFunct(x, orderings[j]) for j in xrange(i+1,len(orderings))])
        crossGroup.extend([mFunct(x, y) for y in orderings2])
    group2 = []
    for i, x in enumerate(orderings2):
        x = GradedPosetSequence(x, isGraded=isGraded, hashableElements=hashableElements)
        group2.extend([mFunct(x, orderings2[j]) for j in xrange(i+1,len(orderings2))])
            

# Kruskall Wallis or Friedman might be used to compare groups, but
# interpretation is a bit iffy.

########################
#   Utility Functions  #
########################
def getMedianValue(values):
    """
    Get the median of a sequence
    Each element of the sequence must be able to be averaged (added and divided by a number)
    @param values: A list of values
    @type values: list of object
    @return: Median value of the list
    @rtype: object
    """
    n = len(values)
    values = sorted(values)
    if n == 0:
        raise IndexError("No median value for empty sequence")
    elif n%2 == 0:
        return (values[int(n/2)] + values[int(n/2-1)])/2.0
    else:
        return values[int((n-1)/2)]

def getValueIndex(value, sequence, isGraded=False, defaultGrade=None):
    """
    Get the index of the given value in the sequence
    @param value: Value to get the position for
    @type value: object
    @param sequence: Nested sequence which is used to determine sorting value of elements
    @type sequence: list of list of object
    @return: Sorting key for the value
    @rtype: int
    """
    if isGraded:
        for i, values in enumerate(sequence):
            isIterable = isinstance(values, VALID_GRADE_CONTAINERS)
            if (isIterable and value in values) or (not isIterable and value == values):
                return i
        return getDefaultIndex(value, i, defaultGrade)
    elif value in sequence:
        return sequence.index(value)
    else:
        return getDefaultIndex(value, len(sequence), defaultGrade)

def getDefaultIndex(element, maxIndex, defaultGrade=None):
    """
    Get a default index for a missing element.
    Default grades are:
    LEFT_GRADE - Always -1, ranked before the lowest existing element(s)
    ZERO_GRADE - Always 0, ranked equal to the lowest element(s)
    MEAN_GRADE - Always half of the maximum grade
    MAX_GRADE - Always equal to the maximum grade, ranked equal to highest element(s)
    RIGHT_GRADE - Always maximum grade +1 than the maximum grade, after the highest element(s)
    @param maxIndex: Maximum possible grade for sequence
    @type maxIndex: int
    @param defaultGrade: The type of default grade to use, from DEFAULT_GRADES set
    @type defaultGrade: str
    @return: Ranking for a default element
    @rtype: int
    """
    if defaultGrade is None:
        raise MissingElementError("%s not a subset element in sequence"%(element,))
    elif defaultGrade == LEFT_GRADE:
        return -1
    elif defaultGrade == ZERO_GRADE:
        return 0
    elif defaultGrade == MEAN_GRADE:
        return maxIndex/2.0
    elif defaultGrade == MAX_GRADE:
        return maxIndex
    elif defaultGrade == RIGHT_GRADE:
        return maxIndex+1
    else:
        raise ValueError("Unknown value for defaultGrade, got: %s"%defaultGrade)

def makeIndexSequence(sequence, referenceSequence, isSeqNested=False, isRefNested=False, tieFunction=sorted,
                      indexFunction=getValueIndex):
    """
    Convert 'sequence' into a sequence of indices from the reference sequence, rather than objects
    Note: This retains the original sequence structure (so if the sequence was nested, it remains nested)
    @param sequence: Sequence to convert into indices
    @type sequence: list of list of object or list of object
    @param referenceSequence: Sequence with "true ordering" used to collect element indices
    @type referenceSequence: list of list of object or list of object
    @param isSeqNested: If True, sequence is nested (where nested elements share a grade)
    @type isSeqNested: bool
    @param isRefNested: If True, reference is nested (where nested elements share a grade)
    @type isRefNested: bool
    @param tieFunction: How to sort elements within the same grade (after applying indices), in form seq = f(seq)
                        The 'sorted' function assumes they are incomparable and removes any inversions.
                        By comparison, a reversed sort would apply an inversion penalty to elements in a grade.
    @type tieFunction: callable
    @param indexFunction: Function for calculating the index of an element, as f(element, referenceSequence, isRefNested)
    @type indexFunction: callable
    @return: The 'sequence' parameter tranformed into integer indices, based on the reference sequence ordering. 
    @rtype: list of list of int or list of int
    """
    if isSeqNested:
        indexSeq = []
        for grade in sequence:
            if isinstance(grade, VALID_GRADE_CONTAINERS):
                indexSeq.append(tieFunction([indexFunction(element,referenceSequence,isRefNested) for element in grade]))
            else:
                indexSeq.append(indexFunction(grade,referenceSequence,isRefNested))
        return indexSeq
    else:
        return [indexFunction(element,referenceSequence,isRefNested) for element in sequence]

def makeFlatIndexSequence(sequence, referenceSequence, isSeqNested=False, isRefNested=False, tieFunction=sorted,
                          indexFunction=getValueIndex):
    """
    Convert 'sequence' into a sequence of indices from the reference sequence,
    Note: This flattens the sequence, if it was nested, for inversion counting.
    rather than objects, then flatten.
    @param sequence: Sequence to convert into indices
    @type sequence: list of list of object or list of object
    @param referenceSequence: Sequence with "true ordering" used to collect element indices
    @type referenceSequence: list of list of object or list of object
    @param isSeqNested: If True, sequence is nested (where nested elements share a grade)
    @type isSeqNested: bool
    @param isRefNested: If True, reference is nested (where nested elements share a grade)
    @type isRefNested: bool
    @param indexFunction: Function for calculating the index of an element, as f(element, referenceSequence, isRefNested)
    @type indexFunction: callable
    @return: Flat sequence of indices, where an element's index is its grade in the reference sequence
    @rtype: list of int
    """
    if isSeqNested:
        indexSeq = []
        for grade in sequence:
            if isinstance(grade, VALID_GRADE_CONTAINERS):
                indexSeq.extend(tieFunction([indexFunction(element,referenceSequence,isRefNested) for element in grade]))
            else:
                indexSeq.append(indexFunction(grade,referenceSequence,isRefNested))
        return indexSeq
    else:
        return [indexFunction(element,referenceSequence,isRefNested) for element in sequence]

def filterElements(sequence, excludedElements, isGraded=False):
    """
    Remove elements from a nested list, if they are part of the excluded elements.
    Returns a copy of the list, in all cases
    @param sequence: Standard sequence ([x,y,...]) or nested sequence ([[x,..], [y,..],..])
    @type sequence: list of object or list of list of object
    @param excludedElements: List of elements to be removed from the sequence
    @type excludedElements: list of object
    @return: Sequence (in same structure) with excluded elements removed
    @rtype: list of object or list of list of object
    """
    if isGraded:
        filtered = []
        for grade in sequence:
            if isinstance(grade, VALID_GRADE_CONTAINERS):
                filteredGrade = [x for x in grade if x not in excludedElements]
                if len(filteredGrade) > 0:
                    filtered.append(filteredGrade)
            elif grade not in excludedElements:
                filtered.append(grade)
        return filtered
    else:
        return [x for x in sequence if x not in excludedElements]
    
