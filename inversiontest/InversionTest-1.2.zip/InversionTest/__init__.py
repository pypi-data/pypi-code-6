"""
InversionTest Package: Inversion Count and Null Hypothesis Test
**************************************************************
Author: Benjamin D. Nye
Description: Library for inversion counting which can adjust for ties and censored data
             (e.g. left censored, right censored, etc). The intention of this library is
             to examine the distance from the sequence of elements to some reference sequence.
             It is also calculates an exact PMF of the distribution for inversion counts under
             the case where all permutations are equally likely, as well as a normal approximation
             for this same distribution.  Wilcoxon and sign tests are provided for hypothesis testing,
             where a group of permutations are compared against a single reference sequence.  This
             sort of testing would be needed for situations where a distribution of collected
             sequences might be compared against a "known correct" reference sequence.

-------------------------------------------------
------   License: Apache License 2.0       ------
-------------------------------------------------
Copyright 2012 Benjamin D. Nye

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---------------------------------------------------
------   Optional 3rd Party Libraries:       ------
---------------------------------------------------
For more efficient test calculations can optionally install:
* SciPy - For scipy.stats binomial and normal cdf functions
"""

import Constants
import InversionAnalysis
import InversionDistribution
import MonteCarloSampler
import StatisticalTests
import PolynomialOperations

# Constants
from Constants import (
    GREATER_THAN_HYPOTHESIS, LESS_THAN_HYPOTHESIS,
    TWO_SIDED_HYPOTHESIS, TEST_HYPOTHESES)
from InversionAnalysis import (
    SIMILARITY_METRIC, EXACT_CDF, NORMAL_CDF, ADAPTIVE_CDF, CDF_TYPES)

# Errors
from InversionAnalysis import InvalidGradedPosetError, MissingElementError
from StatisticalTests import (
    SignTestException, SignTestCancelationError, SignTestInvalidPairLengthError)

# Exposed Classes
from InversionAnalysis import GradedPosetSequence

# Exposed Descriptive Statistics
from InversionAnalysis import (
    inversionCountMax, inversionCountMean, inversionCountVariance, medianSequence)

# Exposed Inversion Count Functions
from InversionAnalysis import (
    inversionCount, mergeSortInversionCount, inversionSimilarity)

# Exposed Probability and Statistics
from InversionAnalysis import (
    inversionCountCDF, inversionSignTest, inversionWilcoxonTest,
    inversionPermutationMeanTest, inversionPermutationRankTest)

# Utility Functions
from InversionAnalysis import filterElements
