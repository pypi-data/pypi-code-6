from delta import setDim, getDim, setIndexRange, getIndexRange, Delta, contractDeltas
from eps import Eps, permute_circular, permute_all, epsAsDeltas
from findIndex import findIndex

from namingSymbols import getNames_aa_ab_ac, getNames_a_aa_aaa, getNewSymbols, getNewSymbols, getNext
from renameIndex import tensorSimplify, subsIndex, renameDummyIndex
from tensor import isTensor, tensorName, longTensorName, TensorFunction, Tensor


from eps import Eps, permute_circular, permute_all, epsAsDeltas



def printStructure(x):
    '''Takes an expression and returns a sring that showes how this epxression is represented as clases and arguments.'''
    if getattr(x, 'args', []):
        return type(x).__name__ + "(" + ", ".join([printStructure(xa) for xa in x.args]) + ")"
    else:
        return str(x)



# To doo list
'''
+ Write unittest for EVERYTHING! 
+ Handle symetric and anti-symetric tensors
+ Fix pretty print
+ Leran about sympy 'assumptions0' and see how to conect to this
'''
