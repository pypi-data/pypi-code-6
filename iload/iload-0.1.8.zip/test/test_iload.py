# -*- coding: utf-8 -*-
import iload


def test_iload_module():
    from test import m
    m1 = iload.iload('test.m')
    assert m is m1 

def test_iload_class():
    from test.m import C
    C1 = iload.iload('test.m.C')
    assert C is C1

def test_iload_func():
    from test.m import f
    f1 = iload.iload('test.m.f')
    assert f is f1


def test_ireload_module():
    from test import m
    m.counter = 0
    iload.ireload(m)
    assert m.counter == 1
    iload.ireload(m)
    assert m.counter == 2

def test_ireload_class():
    from test.m import C
    C1 = iload.ireload(C)
    assert repr(C) == repr(C1)
    assert C is not C1
    from test import m

def test_ireload_func():
    from test.m import f
    f1 = iload.ireload(f)
    assert f is not f1
