import numpy as np
from pydecode.nlp.tagging_train import *
from pydecode.generative import *
from collections import Counter, defaultdict

class GenerativeTagPreprocessor(object):
    def __init__(self, limit=5):
        self.limit = limit

    def preprocess(self, x):
        return np.array([self._map[w] for w in x])

    def initialize(self, X, _, __):
        word_count = Counter()
        for x in X:
            word_count.update(x)
        self._map = defaultdict(lambda:0)
        i = 1
        for w in word_count:
            if word_count[w] > 5:
                self._map[w] = i
                i += 1

        self.n_words = i + 1

class TagProbs(object):
    def __init__(self):
        self._prep = GenerativeTagPreprocessor(5)
        self.components = [self._prep]

    def feature_templates(self, encoder):
        tags = encoder.tags
        self._encoder = encoder
        return [(tags, tags),
                (tags, self._prep.n_words)]

    def output_features(self, x, outputs):
        p = self._prep.preprocess(x)
        o = outputs
        c = BiTagEncoder
        # p(mod | head, dir)
        t = [(o[:, c.PREV_TAG], o[:, c.TAG]),
             (o[:, c.TAG], p[o[:, c.POS]])]
        return t

    def structure(self):
        return [1, 1]

    def pretty_cond(self, template, val):
        return self._encoder.inverse_transform_tag(val[0])



def main():
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = "notebooks/data/wsj_sec_2_21_gold_dependencies"
        X, Y = read_tags(data, 1000, length=20)
        features = TagProbs()
        #print len(X)
        model = BigramModel(features, caching=True)
        ge = GenerativeEstimator(model, max_likelihood)
        # ge.fit(X[:20000], Y[:20000])
        ge.fit_em(X[:500], Y[:500], epochs=20)
        # ge.show()
        #print Y[10], model.inference(X[10], w)
        score(model, ge.w, X[20000:20200], Y[20000:20200])

if __name__ == "__main__":
    main()
