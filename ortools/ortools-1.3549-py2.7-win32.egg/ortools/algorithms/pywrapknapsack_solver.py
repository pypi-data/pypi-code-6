# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.11
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_pywrapknapsack_solver', [dirname(__file__)])
        except ImportError:
            import _pywrapknapsack_solver
            return _pywrapknapsack_solver
        if fp is not None:
            try:
                _mod = imp.load_module('_pywrapknapsack_solver', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pywrapknapsack_solver = swig_import_helper()
    del swig_import_helper
else:
    import _pywrapknapsack_solver
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _pywrapknapsack_solver.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self): return _pywrapknapsack_solver.SwigPyIterator_value(self)
    def incr(self, n=1): return _pywrapknapsack_solver.SwigPyIterator_incr(self, n)
    def decr(self, n=1): return _pywrapknapsack_solver.SwigPyIterator_decr(self, n)
    def distance(self, *args): return _pywrapknapsack_solver.SwigPyIterator_distance(self, *args)
    def equal(self, *args): return _pywrapknapsack_solver.SwigPyIterator_equal(self, *args)
    def copy(self): return _pywrapknapsack_solver.SwigPyIterator_copy(self)
    def next(self): return _pywrapknapsack_solver.SwigPyIterator_next(self)
    def __next__(self): return _pywrapknapsack_solver.SwigPyIterator___next__(self)
    def previous(self): return _pywrapknapsack_solver.SwigPyIterator_previous(self)
    def advance(self, *args): return _pywrapknapsack_solver.SwigPyIterator_advance(self, *args)
    def __eq__(self, *args): return _pywrapknapsack_solver.SwigPyIterator___eq__(self, *args)
    def __ne__(self, *args): return _pywrapknapsack_solver.SwigPyIterator___ne__(self, *args)
    def __iadd__(self, *args): return _pywrapknapsack_solver.SwigPyIterator___iadd__(self, *args)
    def __isub__(self, *args): return _pywrapknapsack_solver.SwigPyIterator___isub__(self, *args)
    def __add__(self, *args): return _pywrapknapsack_solver.SwigPyIterator___add__(self, *args)
    def __sub__(self, *args): return _pywrapknapsack_solver.SwigPyIterator___sub__(self, *args)
    def __iter__(self): return self
SwigPyIterator_swigregister = _pywrapknapsack_solver.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class KnapsackSolver(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KnapsackSolver, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KnapsackSolver, name)
    __repr__ = _swig_repr
    KNAPSACK_BRUTE_FORCE_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_BRUTE_FORCE_SOLVER
    KNAPSACK_64ITEMS_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_64ITEMS_SOLVER
    KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER
    KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER = _pywrapknapsack_solver.KnapsackSolver_KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER
    def __init__(self, *args): 
        this = _pywrapknapsack_solver.new_KnapsackSolver(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _pywrapknapsack_solver.delete_KnapsackSolver
    __del__ = lambda self : None;
    def Init(self, *args): return _pywrapknapsack_solver.KnapsackSolver_Init(self, *args)
    def Solve(self): return _pywrapknapsack_solver.KnapsackSolver_Solve(self)
    def BestSolutionContains(self, *args): return _pywrapknapsack_solver.KnapsackSolver_BestSolutionContains(self, *args)
    def GetName(self): return _pywrapknapsack_solver.KnapsackSolver_GetName(self)
    def use_reduction(self): return _pywrapknapsack_solver.KnapsackSolver_use_reduction(self)
    def set_use_reduction(self, *args): return _pywrapknapsack_solver.KnapsackSolver_set_use_reduction(self, *args)
KnapsackSolver_swigregister = _pywrapknapsack_solver.KnapsackSolver_swigregister
KnapsackSolver_swigregister(KnapsackSolver)

# This file is compatible with both classic and new-style classes.


