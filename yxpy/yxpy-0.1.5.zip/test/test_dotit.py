# -*- coding: utf-8 -*-
from yxpy import dotit


def test_dotdict():
    d = dotit.DotDict(a=1)
    d.b = 2
    assert d.a == 1
    assert d['b'] == 2
    try:
        assert d.c
    except AttributeError:
        pass


def test_dotordereddict():
    d = dotit.DotOrderedDict(a=1)
    d.b = 2
    assert d.a == 1
    assert d['b'] == 2
    assert list(d.keys()) == ['a', 'b']
    try:
        assert d.c
    except AttributeError:
        pass


def test_dotit():
    adict = dict(a=1, b=2)
    d = dotit.DotIt(adict)
    assert d.a == 1
    assert d.b == 2
    try:
        assert d.c
    except AttributeError:
        pass

def test_dotit_nest_dict():
    adict = dict(a=dict(aa=1, ab=2), b=2)
    d = dotit.DotIt(adict)
    assert d.a.aa == 1
    assert d.a.ab == 2
