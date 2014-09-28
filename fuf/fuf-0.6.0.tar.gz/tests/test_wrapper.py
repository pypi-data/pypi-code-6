from __future__ import print_function

from fuf import wrapper


# Test the "decorator decorator"
@wrapper
def myWrapper(f):
    def _wrapped(*args, **kwargs):
        print("Before", args, kwargs)
        ret = f(*args, **kwargs)
        print("After")
        return ret
    return _wrapped

# Sample usage of the custom wrapper
@myWrapper
def myAdd(a, b):
    return a+b

def test_myAdd():
    assert myAdd(1,2) == 3
