"""
Use Case: Hypothetical Simulations of Synthetic Cannabinoid Spread

Note: These simulations are for example use cases only
and are not intended to be an accurate model of any real
situation.  Do not attempt to use these for anything other
than understanding the workings of the InversionTest package.

Author: Benjamin D. Nye
License: Apache License V2.0
"""

def readSimulationResults(fileName, rowSep='\n', colSep=',', gradeSep=';'):
    """
    Read the simulation results from a CSV-formatted file.
    A file with the data:
    "Element1,Element2,Element3;Element4,Element5\nElement1,Element5"
    Corresponds to the graded sequences:
    [[["Element1"], ["Element2"], ["Element3", "Element4"], ["Element5"]],
     [["Element1"], ["Element5"]]]
    @param fileName: Name of the input file to read the simulation results
    @type fileName: str
    @param rowSep: Separator for rows.  For CSV, should be '\n' or '\r'
    @type rowSep: str
    @param colSep: Separator for columns.  For CSV, should be ','
    @type colSep: str
    @param gradeSep: Separator for grades within a cell.
    @type gradeSep: str
    @return: List of graded permutations, in the form [permutation1, permutation2, ...]
    @rtype: list of list of list of str
    """
    with open(fileName, 'r') as inFile:
        data = inFile.read()
    results = [[[x for x in grade.split(gradeSep)] for grade in result.split(colSep)]
               for result in data.split(rowSep)]
    return results

if __name__ == '__main__':
    from InversionTest import (inversionWilcoxonTest, inversionSignTest,
                               inversionPermutationMeanTest,
                               inversionPermutationRankTest,
                               inversionSimilarity, inversionCountCDF,
                               medianSequence)

    def average(vals):
        """ Average the given values """
        return float(sum(vals))/len(vals)

    # Actual Ordering to Compare Against
    GROUND_TRUTH_ORDER = ['BX', 'DY', 'AU', 'BW', 'AW',
                             'AV', 'AX', 'CX', 'BY', 'BV',
                             'AY', 'BZ', 'AZ', 'CW', 'CY',
                             'DZ', 'CZ', 'DX', 'BU', 'CV',
                             'CU', 'EX', 'EY', 'DV',
                             ['DU', 'DW', 'EU', 'EV', 'EW', 'EZ']]
    
    # Constants
    localSimFileName = 'LocalizedSimResults.csv'
    mediaSimFileName = 'MediaSimResults.csv'
    
    # Load Data: A list of graded sequences
    localResults = readSimulationResults(localSimFileName)
    mediaResults = readSimulationResults(mediaSimFileName)
    
    # Perform Analyses
    localWilcoxonPValue   = inversionWilcoxonTest(localResults, seq=GROUND_TRUTH_ORDER, isGraded=True)
    localAvgCDFComplement = average([1-inversionCountCDF(GROUND_TRUTH_ORDER, result, isGraded=True)
                                     for result in localResults])
    localAvgSimilarity    = average([inversionSimilarity(GROUND_TRUTH_ORDER, result, isGraded=True)
                                     for result in localResults])
    localMedianSeq = medianSequence(localResults, isGraded=True)
    localMedianSimilarity = inversionSimilarity(GROUND_TRUTH_ORDER, localMedianSeq, isGraded=True)
    
    mediaWilcoxonPValue   = inversionWilcoxonTest(mediaResults, seq=GROUND_TRUTH_ORDER, isGraded=True)
    mediaAvgCDFComplement = average([1-inversionCountCDF(GROUND_TRUTH_ORDER, result, isGraded=True)
                                     for result in mediaResults])
    mediaAvgSimilarity    = average([inversionSimilarity(GROUND_TRUTH_ORDER, result, isGraded=True)
                                     for result in mediaResults])
    mediaMedianSeq = medianSequence(mediaResults, isGraded=True)
    mediaMedianSimilarity = inversionSimilarity(GROUND_TRUTH_ORDER, mediaMedianSeq, isGraded=True)

    twoSampleWilcoxonPValue = inversionWilcoxonTest(localResults, mediaResults,
                                                    seq=GROUND_TRUTH_ORDER, isGraded=True)
    twoSampleSignPValue = inversionSignTest(localResults, mediaResults,
                                          seq=GROUND_TRUTH_ORDER, isGraded=True)
    twoSamplePMeanPValue = inversionPermutationMeanTest(localResults, mediaResults,
                                                        seq=GROUND_TRUTH_ORDER, isGraded=True)
    twoSampleRMeanPValue = inversionPermutationRankTest(localResults, mediaResults,
                                                        seq=GROUND_TRUTH_ORDER, isGraded=True)

    # Print Results
    print "Localized Simulation Analysis"
    print "*"*30
    print "   Wilcoxon P-Value:   %.2e"%localWilcoxonPValue
    print "   Average 1-CDF:      %.2f"%localAvgCDFComplement  
    print "   Average Similarity: %.2f"%localAvgSimilarity                                         
    print "   Median Similarity:  %.2f"%localMedianSimilarity
    print
    print "Media Simulation Analysis"
    print "*"*30
    print "   Wilcoxon P-Value:   %.2e"%mediaWilcoxonPValue
    print "   Average 1-CDF:      %.2f"%mediaAvgCDFComplement
    print "   Average Similarity: %.2f"%mediaAvgSimilarity 
    print "   Median Similarity:  %.2f"%mediaMedianSimilarity
    print
    print "Two Population Tests (Alternate Hypothesis: Local > Media)"
    print "*"*30
    print "   Wilcoxon P-Value:   %.2e"%twoSampleWilcoxonPValue
    print "   Sign Test P-Value:  %.2e"%twoSampleSignPValue
    print "   Permutation Means P-Value:   %.2e"%twoSamplePMeanPValue
    print "   Permutation Ranks P-Value:  %.2e"%twoSampleRMeanPValue
