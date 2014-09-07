from InversionTest import inversionSimilarity
referenceSeq 		= [1, 2, 3, 4, 5, 6]
fullyObserved     = [1, 2, 4, 3, 6, 5] 
rightCensored     = [1, 2, 4, [3, 6, 5]] 
leftCensored      = [[1, 2, 4], 3, 6, 5] 
intervalCensored  = [1, [2, 4], [3, 6], 5]
fullSim = inversionSimilarity(fullyObserved, referenceSeq)
rCensoredSim = inversionSimilarity(rightCensored, referenceSeq, 
                                   isGraded = True)
lCensoredSim = inversionSimilarity(leftCensored, referenceSeq, 
                                   isGraded = True)
iCensoredSim = inversionSimilarity(intervalCensored, referenceSeq, 
                                   isGraded = True)
print "Fully Observed Similarity:", fullSim
print "Right Censored Similarity:", rCensoredSim
print "Left Censored Similarity:", lCensoredSim
print "Interval Censored Similarity:", iCensoredSim
