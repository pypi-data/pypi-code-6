# -*- coding: utf-8 -*-
from yxpy import loadit


def test_loadit_module():
    from test.data.loadit import m
    m1 = loadit.load_it('test.data.loadit.m')
    assert m is m1 

def test_loadit_class():
    from test.data.loadit.m import C
    C1 = loadit.load_it('test.data.loadit.m.C')
    assert C is C1

def test_loadit_func():
    from test.data.loadit.m import f
    f1 = loadit.load_it('test.data.loadit.m.f')
    assert f is f1


def test_ireload_module():
    from test.data.loadit import m
    m.counter = 0
    loadit.reload_it(m)
    assert m.counter == 1
    loadit.reload_it(m)
    assert m.counter == 2

def test_ireload_class():
    from test.data.loadit.m import C
    C1 = loadit.reload_it(C)
    assert str(C) == str(C1)
    assert C is not C1

def test_ireload_func():
    from test.data.loadit.m import f
    f1 = loadit.reload_it(f)
    assert f is not f1
