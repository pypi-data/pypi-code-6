import sympy.core.cache

# Why doesn't it work to use "import sympy.core.compatibility" and call "with_metaclass" as "sympy.core.compatibility.with_metaclass"?
from sympy.core.compatibility import with_metaclass
from sympy.core.function import AppliedUndef, FunctionClass
from sympy.core.core import BasicMeta
from sympy.core.assumptions import ManagedProperties
from sympy.core.cache import cacheit



'''
Tensor('name') creates a tensor that does not take arguments
>>> T = Tensor('T')
>>> T(*index)

TensorFunction creates a teonsr that do take arguments
>>> TF = TensorFunction('TF')
>>> TF(*index)(*args)

Both Tensor and TensorFuncton takes any number of index. Anytning can be put as an index but only indices of type sympy.Dummy or sympy.Symbol will be contracted over in varios functions.

>>> a=sympy.Dymmy('a'); b=sympy.Dymmy('b')
>>> isinstance(Tensor('T')(a,b), sympy.Symbol)
True

>>> a=sympy.Dymmy('a'); b=sympy.Dymmy('b')
>>> isinstance(TensorFunction('TF')(a,b), sympy.FunctionClass)
True

>>> a=sympy.Dymmy('a'); b=sympy.Dummy('b); 
>>> x=sympy.Symbol('x')
>>> isinstance(TensorFunction('TF')(a,b)(x), sympy.Function)
True
'''




def isTensor(exp):
    '''Test if exp is a Tensor or TensorFunction. 
       Only returns True for Tensor with index/indecis and TensorFunction with index/indecis and argument(s)
       Only test the top type of exp, e.g. does not detect a derivative of a tensor as a tensor'''
    return (isinstance(exp,(AppliedTensor, 
                            AppliedAppliedTensorFunction)))


def tensorName(exp):  
    '''Writes exp a sring as a sring, without indices, without arguments.'''
    if isinstance(exp,AppliedTensor):
        return type(exp).__name__
    if isinstance(type(exp),AppliedTensorFunction):
        return type(type(exp)).__name__
    if hasattr(exp,'args'):
        return type(exp).__name__
    return str(exp)



def longTensorName(exp):  
    '''Writes exp a sring as a sring, without indices, with arguments.'''
    if isinstance(exp,AppliedTensor):
        return type(exp).__name__
    if isinstance(type(exp),AppliedTensorFunction):
        return (type(type(exp)).__name__ 
                + "(" 
                + ", ".join([longTensorName(arg) for arg in exp.args]) 
                + ")" )
    if getattr(exp, 'args', []):
        return (type(exp).__name__ 
                + "(" 
                + ", ".join([longTensorName(arg) for arg in exp.args]) 
                + ")" )
    return str(exp)


# Defines what types of indices that can be contracted over
def isAllowedDummyIndex(ind):
    '''Returns True if object is allowed to use as a dummy index to be summed over acording to Einsteins sumation convention'''
    return isinstance(ind, (sympy.Symbol, sympy.Dummy) )


def withNewIndex(tensor,index):
    if isTensor(tensor):
        return tensor.withNewIndex(*index)
    return tensor


class TensorFunction(BasicMeta):
    @cacheit
    def __new__(mcl, name, *arg, **kw):
        if (name == "AppliedTensorFunction"):
            return type.__new__(mcl, name, *arg, **kw)
        return type.__new__(mcl, name, (AppliedTensorFunction,), kw)
    def __init__(self, *arg, **kw):
        pass


#FIXME use sympy.core.compatibility.with_metaclass or similar
class AppliedTensorFunction(FunctionClass):
    __metaclass__ = TensorFunction

    @cacheit
    def __new__(mcl, *index, **kw):
        name = mcl.__name__ + str(index)
        ret = type.__new__(mcl, name, (AppliedAppliedTensorFunction,AppliedUndef),kw)
        ret.index = index
        return ret
    is_Tensor = True


class AppliedAppliedTensorFunction(AppliedUndef):
    def withNewIndex(self, *index):
        return type(type(self))(*index)(*self.args)
        

class Tensor(ManagedProperties):
    @cacheit
    def __new__(mcl, name, *arg, **kw):
        if (name == "AppliedTensor"):
            return type.__new__(mcl, name, *arg, **kw)
        return type.__new__(mcl, name, (AppliedTensor,),kw)


#FIXME use sympy.core.compatibility.with_metaclass or 
class AppliedTensor(sympy.Symbol):
    __metaclass__ = Tensor

    @cacheit
    def __new__(cls, *index, **kw):
        name = cls.__name__ + str(index)
        ret = sympy.Symbol.__new__(cls, name, **kw)  
        ret.index = index
        return ret
    is_Tensor = True


    def withNewIndex(self,*index):
        return type(self)(*index)




##################### Here be unittest #####################
import unittest

class TestTensor(unittest.TestCase):

    def setUp(self):
        self.t = Tensor('t')
        self.T = Tensor('t')
        self.tf = TensorFunction('tf')
        self.TF = TensorFunction('tf')
        self.a = sympy.Dummy('a')
        self.b = sympy.Dummy('b')
        self.x = sympy.Symbol('x')
        self.f = sympy.Function('f')

    def test_classRelations(self):
        t=self.t; tf=self.tf; a=self.a; b=self.b; x=self.x
        self.assertEqual( type(t), Tensor )
        self.assertEqual( type(t(a,b)), t )
        self.assertEqual( type(t(a,b)).__base__, AppliedTensor )
        self.assertTrue( isinstance(t(a,b), sympy.Symbol))
        self.assertEqual( type(tf(a,b)), tf )
        self.assertEqual( type(tf(a,b)).__base__, AppliedTensorFunction )
        self.assertTrue( isinstance(tf(a,b), sympy.FunctionClass) )
        self.assertEqual( type(tf(a,b)(x)), tf(a,b) )
        self.assertEqual( type(tf(a,b)(x)).__base__, AppliedAppliedTensorFunction )
        self.assertTrue( isinstance(tf(a,b)(x), AppliedUndef) )
        self.assertTrue( isinstance(tf(a,b)(x), sympy.Function) )

    def test_withNewIndex(self):
        t=self.t; tf=self.tf; a=self.a; b=self.b; x=self.x  
        self.assertEqual( t(a).withNewIndex(b,b), t(b,b) )
        self.assertEqual( tf(a)(x).withNewIndex(b,b), tf(b,b)(x) )

    def test_isTensor(self):
        t=self.t; tf=self.tf; a=self.a; b=self.b; x=self.x; f=self.f
        self.assertFalse( isTensor(a) )
        self.assertFalse( isTensor(f(x)) )
        self.assertTrue( isTensor(t(a,b)) )
        self.assertTrue( isTensor(tf(a,b)(x,x)) )

    def test_eqality(self):
        t=self.t; tf=self.tf; a=self.a; b=self.b; x=self.x; TF=self.TF; T=self.T
        self.assertEqual( t(a), T(a) )
        self.assertNotEqual( t(b), t(a) )
        self.assertEqual( tf(a)(x,b), TF(a)(x,b) )
        self.assertNotEqual( tf(a)(x,b), tf(a)(x,x) )
        self.assertNotEqual( tf(a)(x,b), tf(b)(x,b) )

if __name__ == '__main__':
    unittest.main()

