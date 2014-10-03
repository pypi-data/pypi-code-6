import delta
import tensor
import sympy


'''
Eps is the Levi-Civita symbol, also known as the maximaly antisymetric tensor.

Make sure that the number of indecis matches the number of dimensions.
'''



class Eps(tensor.AppliedTensor):
    pass


def oddEven(num):
    '''returns 1 if num is even, returns -1 if num is odd'''
    if num%2: return -1
    return 1
        
# is not used at the moment
def permute_circular(theList):
    '''returns all circular permutations of theList'''
    perms = []
    for i in range(len(theList)):
        perms.append(list(theList))
        theList.insert(0,theList.pop())
    return perms
    

def permute_all(theList):
    '''returns all permutations of theList and their parity'''
    theList = list(theList)
    lenList = len(theList)
    if lenList < 2:
        return [{'perm':theList,'parity':1}]
    oddEvenList = oddEven(lenList)
    perms=[]
    for (pos,obj) in enumerate(theList):
        short = theList[0:pos]+theList[pos+1:lenList]
        oddEvenPos = oddEven(pos+1)
        for perm in permute_all(short):
            perm['perm'].append(obj)
            perm['parity'] *= oddEvenList * oddEvenPos
            perms.append(perm)
    return perms
        

def oneEpsAsDeltas(eps, **tempOverride):
    '''Takes an instance of Eps and rewrites it as Deltas'''
    dim, indexRange = delta.getTempDimAndIndexRange(**tempOverride)
    if not isinstance(eps,Eps):
        raise TypeError('Error: input must be an Eps(*indecis)')
    if not len(eps.index)==dim:
        raise TypeError('Error: Eps must have dim number of indices')
    termList=[]
    for perm in permute_all(eps.index):
        factorList=[ perm['parity'] ]
        for (pos,index) in enumerate(perm['perm']):
            factorList.append( delta.Delta(pos+1,index) )
        termList.append(sympy.Mul(*factorList))  
    return sympy.Add(*termList)



def epsAsDeltas(exp, **kw):
    '''Takes an epression, and rewrites all Eps as Deltas'''
    if isinstance(exp,Eps):
        return oneEpsAsDeltas(exp, **kw)
    if not getattr(exp,'args',()):
        return exp
    return type(exp)(*[epsAsDeltas(arg, **kw) for arg in exp.args])
    

def simplify_OneEps(eps, evalLevel=2, **tempOverride):
    '''Takes an instance of Eps and tries to simplify. Returns 0 if any two indecis are equal. Rewrite eps as Deltas if the number of loose idecis (not in indexRange) of eps is equal to or less than evalLevel.'''
    indexRange = delta.getTempDimAndIndexRange(**tempOverride)[1]
    if not isinstance(eps,Eps):
        raise TypeError('Error: input must be an Eps(*indecis)')
    ints = 0
    for (pos,ind) in enumerate(eps.index):
        if ind in eps.index[ind+1:]:
            return 0
        if ind in indexRange:
            if ind>len(eps.index) or ind<1:
                ints += 1
    if len(eps.index) - ints > evalLevel:
        return eps
    return delta.contractDeltas(epsAsDeltas(eps, **tempOverride),
                                **tempOverride)
        


 


##################### Here be unittest #####################
import unittest
from delta import Delta, getDim, setDim
import sympy


class TestEps(unittest.TestCase):

    def setUp(self):
        pass




if __name__ == '__main__':
    unittest.main()

