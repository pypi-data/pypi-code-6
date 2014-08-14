


class BigramModel(pydecode.model.HammingLossModel,
                  pydecode.model.DynamicProgrammingModel):
    def dynamic_program(self, x):
        n = len(x)
        if ("DP", n) not in self.cache:
            graph, encoder = pydecode.nlp.tagger(
                n, [1] + [self._encoder.tags] * len(x)-2 + [1])
            self.cache["DP", n] = (graph, encoder)
        else:
            return self.cache["DP", n]

    def initialize(self, X, Y):
        # Initialize the tag set.
        tags = set()
        for y in Y:
            for tag in y:
                tags.add(y)
        self.n_tags = len(tags)

        # Initialize the preprocessor.
        self.preprocessor = Preprocesser()
        for x in X:
            for word in x:
                self.preprocessor.add(self._preprocess_word(w))

    def _preprocess_word(self, word):
        return {"SUFF1": word[-1:],
                "SUFF2": word[-2:],
                "SUFF3": word[-3:],
                "PRE1": word[:1],
                "PRE2": word[:2],
                "PRE3": word[:3],
                "WORD": word}

    def templates(self):
        def s(t):
            return self.size(t)
        n_tags = self.n_tags
        return [(n_tags, s("WORD")),
                (n_tags, s("SUF1")),
                (n_tags, s("SUF2")),
                (n_tags, s("SUF3")),
                (n_tags, s("PRE1")),
                (n_tags, s("PRE2")),
                (n_tags, s("PRE3")),
                (n_tags, n_tags)]

    def label_features(self, x, outputs):
        if ("PP", x) in self.cache:
            p = self.cache["PP", x]
        else:
            p = self.preprocessor.transform(
                [self._preprocess_word(word)
                 for word in x])
            self.cache["PP", x] = p

        pos = outputs[:, 0]
        tag = outputs[:, 2]
        return [(tag, p["WORD"][pos]),
                (tag, p["SUF1"][pos]),
                (tag, p["SUF2"][pos]),
                (tag, p["SUF3"][pos]),
                (tag, p["PRE1"][pos]),
                (tag, p["PRE2"][pos]),
                (tag, p["PRE3"][pos]),
                (tag, outputs[:,1])]

def train_and_save(model, X, Y, f="/tmp/weights.npy"):
    sp = StructuredPerceptron(model, verbose=1, max_iter=10, average=True)
    sp.fit(X, Y)
    np.save(f, sp.w)

def load_and_test(model, X_test, Y_test, f="/tmp/weights.npy"):
    w = np.load(f)
    total = []
    correct = []
    for x, y in zip(X_test, Y_test):
        total += list(model.inference(x, w))
        correct += list(y)
    print sklearn.metrics.hamming_loss(all, correct)

def read_tags(f, limit, length):
    data = "notebooks/data/wsj_sec_2_21_gold_dependencies"
    records = nlpformat.read_csv_records(data, limit=limit, length=length)
    f = nlpformat.CONLL
    return zip(*[(("*START*",) + tuple(record[:, f["WORD"]]) + ("*END*",),
                  ("*START*",) + tuple(record[:, f["TAG"]]) + ("*START*",))
                 for record in records])

def score(model, w, X, Y):
    right = []
    wrong = []
    for x, y in zip(X, Y):
        yhat = model.inference(x, w)
        right += y
        wrong += yhat
    print model.loss(right, wrong)

def main():
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        X, Y = read_tags("notebooks/data/wsj_sec_2_21_gold_dependencies")
        features = BetterBigramFeatures()
        model = BigramModel(features, DictionaryPruner())

        # X = X[:1000]
        # Y = Y[:1000]
        train_and_save(model, X[:500], Y[:500], "q_test")

if __name__ == "__main__":
    main()

        # data_X = [["*START*"] + sentence.split() + ["*END*"]  for sentence in
        #           ["the dog walked",
        #            "in the park",
        #            "in the dog"]]
        # data_Y =  [["*START*"] + tags.split() + ["*START*"]
        #            for tags in ["D N V", "I D N", "I D N"]]
        # coder = pydecode.nlp.tagging.BiTagCoder()
        # coder.fit(data_Y)
        # model = BigramModel(coder, SimpleBigramFeatures(coder))
        # sp = StructuredPerceptron(model, verbose=1, max_iter=10)
        # sp.fit(data_X, data_Y)


        # prep = TaggingPreprocessor()
        # prep.initialize(data_X)
        # model = BigramModel(coder, BetterBigramFeatures(coder, prep))
        # sp = StructuredPerceptron(model, verbose=0, max_iter=10)
        # sp.fit(data_X, data_Y)
        # data = "notebooks/data/wsj_sec_2_21_gold_dependencies"
        # records = format.read_csv_records(data, [], [])

        # # sents = [zip(*sentence) for sentence in conll_sentences(
        # # sents = [zip(*sentence) for sentence in sentences("notebooks/data/tag_train_small.dat")]

        # f = format.CONLL
        # X, Y = zip(*[(("*START*",) + tuple(record[:, f["WORD"]]) + ("*END*",),
        #               ("*START*",) + tuple(record[:, f["TAG"]]) + ("*START*",))
        #              for record in records])

        # features = BetterBigramFeatures()
        # model = BigramModel(features, DictionaryPruner())

        # # X = X[:1000]
        # # Y = Y[:1000]
        # train_and_save(model, X[:1000], Y[:1000], "q_test")
        # # train_and_save(X[:39000], Y[:39000], "q")
        # # load_and_test(X, Y, X[5000:5600], Y[5000:5600])
