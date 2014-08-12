"""
Implements CCM-like model using dependency parsing.

Dan Klein and Chris Manning
A Generative Constituent-Context Model forImproved Grammar Induction, 2002
"""
import pydecode.nlp.dependency_parsing as dep
import numpy as np
from pydecode.nlp.dependency_parsing_train import *
from pydecode.generative import *

class DepProbs(object):
    ENC = ParsingPreprocessor
    def __init__(self):
        self._prep = self.ENC()
        self.components = [self._prep]

    def feature_templates(self, _):
        def size(t):
            return self._prep.size(t) + 1
        return [(size(self.ENC.TAG), 2, size(self.ENC.TAG))]

    def output_features(self, x, outputs):
        p = self._prep.preprocess(x)
        o = outputs
        c = dep.FirstOrderCoder
        # p(mod | head, dir)
        t = [(p[self.ENC.TAG][o[:, c.HEAD]],
              o[:, c.MOD] < o[:, c.HEAD],
              p[self.ENC.TAG][o[:, c.MOD]])]
        return t

    def structure(self, _):
        return [1]
        # def size(t):
        #     return self._prep.size(t) + 1

def main():
    data = "notebooks/data/wsj_sec_2_21_gold_dependencies"
    records = nlpformat.read_csv_records(data,
                                     limit=10,
                                     length=50)
    f = nlpformat.CONLL

    X, Y = [], []
    for record in records:
        X.append(DepX(("*ROOT*",) + tuple(record[:, f["WORD"]]),
                      ("*ROOT*",) + tuple(record[:, f["TAG"]])))
        parse = dep.DependencyParse((-1,) + tuple(map(int, record[:, f["HEAD"]])))
        Y.append(parse)

    features = DepFeatures()
    model = FirstOrderModel(features)
    estimate(model, X, Y, max_likelihood)

if __name__ == "__main__":
    main()
