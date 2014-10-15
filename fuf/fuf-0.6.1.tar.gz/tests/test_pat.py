import sys # For module support
from fuf import *
# Testing out

def test_abs():

    @Overload(ge(0))
    def _abs(x):
        return x

    @Overload(lt(0))
    def _abs(x):
        return -x

    assert _abs(10) == 10, "First overload"
    assert _abs(-10) == 10, "Fell back"

def test_sum():
    @Overload(len)
    def _sum(lst):
        return lst[0] + _sum(lst[1:])

    @Overload()
    def _sum(lst):
        return 0

    assert _sum(range(6)) == 15, "Primitive predicate failure"

def test_is():
    @Overload(int)
    def isint(x):
        return True

    @Overload()
    def isint(x):
        return False

    assert isint(5), "Is predicate failed"
    assert not isint(5.0), "Is predicate failed"

def test_manual():
    manual = OverloadSet()

    @manual.reg(lt(2))
    def fact(x):
        return 1

    @manual.reg()
    def fact(x):
        return x * fact(x-1)

    assert fact(6) == 720, "Manual registration failed"

def test_exists():
    @Overload(stuff=Any)
    def tryit(**kwargs):
        return True

    @Overload()
    def tryit(**kwargs):
        return False

    assert tryit(stuff=""), "Did not detect keyword argument"
    assert not tryit(), "Detected nonexistant keyword argument"

def test_complex():
    @Overload(And(gt(5), lt(10)))
    def getval(x):
        return True

    @Overload(Or(lt(5), gt(10)))
    def getval(x):
        return False

    assert getval(6), "And statement failed"
    assert not getval(2), "Or statement failed"
