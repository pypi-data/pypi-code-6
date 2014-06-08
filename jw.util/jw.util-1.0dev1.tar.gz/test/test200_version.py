"""
Test version module
"""
from util import version

def test1():
    """
    Test constructor
    """
    v = version.Version('1.0')
    assert v.version == [1, 0]

def test2():
    """
    Test incrementing
    """
    v = version.Version('1.0')
    v.incr()
    assert v.version == [1, 1]

def test3():
    """
    Test incrementing
    """
    v = version.Version('1.0')
    v.decr()
    assert v.version == [1, -1]

def test3():
    """
    Test incrementing at higher level
    """
    v = version.Version('1.0')
    v.incr(-2)
    assert v.version == [2]
