# -*- coding: utf-8 -*-
from yxpy.maybestartswith import maybe_startswith


def test_maybestartswith_yes():
    assert maybe_startswith(b'abcd', b'-', b'abc') == True

def test_maybestartswith_no():
    assert maybe_startswith(b'ad', b'-', b'abc') == False

def test_maybestartswith_not_sure():
    assert maybe_startswith(b'ab', b'-', b'abc') == None
