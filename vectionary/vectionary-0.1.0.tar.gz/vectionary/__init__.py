from collections import Counter


class VectorDict(dict):

    def __mul__(self, other):
        return Counter(dict((k, v * other) for k, v in self.iteritems()))

    def magnitude(self):
        return self.inner_product(self) ** .5

    def inner_product(self, other):
        if not isinstance(other, VectorDict):
            raise NotImplementedError
        return sum(v * other.get(k, 0) for k, v in self.iteritems())

    def jaccard_similarity(self, other):
        s1 = frozenset(self.keys())
        s2 = frozenset(other.keys())
        unionsize = len(s1 | s2)
        if unionsize == 0:
            return 0
        return len(s1 & s2) / float(unionsize)

    def cosine_similarity(self, other):
        if not isinstance(other, VectorDict):
            raise NotImplementedError
        sl = self.magnitude()
        ol = other.magnitude()
        if sl == 0 or ol == 0:
            return 0
        return self.inner_product(other) / float(sl) / float(ol)

    __rmul__ = __mul__


class VectorCounter(VectorDict, Counter):
    pass


def vectordict_ducktest(maybe_vectordict):
    C = maybe_vectordict
    assert C(a=2) * 5 == C(a=10)
    assert 5 * C(a=2) == C(a=10)
    assert C(a=2) * 5 == C(a=10)
    assert C(a=2).magnitude() == 2
    assert 2.23 < C(a=1, b=2).magnitude() < 2.24
    assert 4 == C(a=3, b=2).inner_product(C(b=2, c=3))
    assert 0.707 < C(a=2).cosine_similarity(C(a=1, b=1)) < 0.708
    assert .25 == C(a=1, b=1).jaccard_similarity(C(b=1, c=1, d=1))
    assert C().cosine_similarity(C(a=1, b=1)) == 0
    assert C(a=1, b=1).cosine_similarity(C()) == 0
    assert C().cosine_similarity(C()) == 0
    assert C().jaccard_similarity(C(a=1, b=1)) == 0
    assert C(a=1, b=1).jaccard_similarity(C()) == 0
    assert C().jaccard_similarity(C()) == 0
