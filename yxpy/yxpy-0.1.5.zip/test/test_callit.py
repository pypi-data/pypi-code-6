# -*- coding: utf-8 -*-
from yxpy.callit import CallIt


def setup_module():
    global acall
    acall = CallIt(3.1415926, '.2f')

def test_call_constructor():
    assert acall.args == (3.1415926, '.2f')
    assert acall.kwargs == {}

def test_call_function():
    assert acall(format) == format(3.1415926, '.2f')
