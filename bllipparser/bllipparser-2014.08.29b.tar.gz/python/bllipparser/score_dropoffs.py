import math
from RerankerFeatureCorpus import RerankerFeatureCorpus

corpus = RerankerFeatureCorpus('/home/dmcc/rev/bllip-parser-new-optimizer/second-stage/features/ec50spnonfinal/dev.gz')
for sentence in corpus:
    for i, parse in enumerate(sentence.parses):
        score = parse.features.get(0, 0)
        print i, math.exp(-score)
    print
