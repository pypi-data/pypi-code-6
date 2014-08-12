class Preprocessor(object):
    def initialize(self, X):
        pass

    def preprocess(self, X):
        return X

class Pruner(object):
    def initialize(self, X, Y, out):
        pass

    def preprocess(self, x):
        return X


class StructuredCoder(object):
    def inverse_transform(self, outputs):
        pass

    def transform(self, y):
        pass
