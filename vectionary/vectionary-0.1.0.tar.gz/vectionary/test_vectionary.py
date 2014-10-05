from collections import Counter
from . import VectorDict, VectorCounter, vectordict_ducktest


def test():
    assert issubclass(VectorDict, dict)
    assert issubclass(VectorCounter, dict)
    assert issubclass(VectorCounter, Counter)
    assert issubclass(Counter, dict)

    for cls in (VectorDict, VectorCounter):
        vectordict_ducktest(cls)
