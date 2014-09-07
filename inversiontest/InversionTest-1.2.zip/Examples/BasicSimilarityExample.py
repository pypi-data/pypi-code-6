from InversionTest import inversionSimilarity
A, B, C, D = object(), object(), object(), object()
sequence1 = [[D, A], C, B] 
sequence2 = [A, B, [C, D]]
similarity = inversionSimilarity(sequence1, sequence2, 
                                 isGraded = True)
print "Similarity:", similarity
