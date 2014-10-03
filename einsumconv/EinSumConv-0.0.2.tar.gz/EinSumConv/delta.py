import tensor
import lists
import sympy


'''
<!> Always use sympy.expand(exp) before using makeTermList(exp) <!>
If you ignore this recomendation, stuf might not work as expcted.

Delta is the Kronicer delta.

ContractDeltas contracts all idndices of all Deltas, that are sympy.Symbol or sympy.Dummy

>>> T=tensor.Tensor('T')
>>> a,b,c,d = sympy.symbols('a,b,c,d')
>>> contractDeltas(Delta(a,c)*Detla(b,d)*T(c,d))

dim is the number of dimensions of the indecis.
>>> constracDeltas(Delta(a,a)) == dim
True

setDim canges dim. Dim is originaly set to 4
>>> dim
4
>>> setDim(4711)
>>> dim
4711

dim can be overrided in spesific calculations
>>> setDim(4)
>>> constracDeltas(Delta(a,a), dim=13)
13

'''



global dim
dim = 3

global indexRange
indexRange = [1, 2, 3]


    

def setDim(newDim):
    '''Sets number of dimensions'''
    global dim
    dim = newDim
    if not len(indexRange) == dim:
        setIndexRange(range(1,1+dim))

def getDim():
    '''returns number of dimensions'''
    return dim

def setIndexRange(newIndexRange):
    '''Sets what values of indecis to be formaly summed over.
       e.g. in 3D vecor calculations: indexRange = [1,2,3]
       e.g. in relativistic calculations: indexRange = [0,1,2,3]'''
    global indexRange
    indexRange = newIndexRange
    dim = len(indexRange)
    setDim(dim)
    if (not isinstance(indexRange[0], (int, sympy.Integer))
            or not isinstance(indexRange[0], (int, sympy.Integer))
            or not range(indexRange[0],indexRange[dim-1]+1) == indexRange ):
        return "Warning: str(indexRange) is a verry bad indexRange"

def getIndexRange():
    return indexRange


def getTempDimAndIndexRange(**tempOverride):
    if 'dim' in tempOverride:
        dim = tempOverride['dim']
        if 'indexRange' in tempOverride:
            indexRange = tempOverride['indexRange']
            if not dim == len(indexRange):
                raise TypeError('indexRange must have length dim')
        else: indexRange = range(1,dim+1)
    elif 'indexRange' in tempOverride:
        indexRange = tempOverride['indexRange']
        dim = len(indexRange)
    else:
        dim = getDim()
        indexRange = getIndexRange()
    return dim, indexRange




class Delta(tensor.AppliedTensor):
    pass



def contractOneDelta(factorList, **tempOverride):
    dim, indexRange = getTempDimAndIndexRange(**tempOverride)
    newFactorList=list(factorList)
    for (i,D) in enumerate(factorList):
        if not isinstance(D,Delta):
            continue
        
        if not len(getattr(D,'index',[]))==2:
            raise TypeError('Error: delta must have precisly two indices')
        d1,d2 = D.index
        if not (tensor.isAllowedDummyIndex(d1)
                or tensor.isAllowedDummyIndex(d2)):
            if (d1 in indexRange) and (d2 in indexRange):
                if d1==d2: newFactorList[i]=1
                else: newFactorList[i]=0    
                return newFactorList
            continue
        
        if d1==d2:
            newFactorList[i]=dim
            return newFactorList
        
        for (j,factor) in enumerate(factorList):
            if i==j: continue
            if isinstance(factor,tensor.AppliedTensor):
                indexList=list(factor.index)
                if not deltaReplace(indexList,d1,d2):
                    continue
                newFactorList[j]=factor.withNewIndex(*indexList)
                newFactorList[i]=1
                return newFactorList

            if not hasattr(factor,'args'): continue

            indexDict, indexList = lists.serchIndexInFactor(factor)
            if not deltaReplace(indexList,d1,d2):
                continue
            newFactorList[j] = lists.withNewIndex(
                                    factor, indexDict, indexList)
            newFactorList[i] = 1
            return newFactorList
    return None



def deltaReplace(theList,d1,d2):
    '''Replace index d1 with d2 or d2 with d1 in theList, if possible.
       Only replace if the index that is replaced is an allowed dummy index
       return True if replacement was made, replace False otherwise.'''
    for (i,obj) in enumerate(theList):
        if tensor.isAllowedDummyIndex(d1) and obj==d1:
            theList[i]=d2
            return True
        if tensor.isAllowedDummyIndex(d2) and obj==d2:
            theList[i]=d1
            return True
    return False


def contractDeltas_factorList(factorList, *arg, **kw):
    while True:
        newFactorList=contractOneDelta(factorList, *arg, **kw)
        if newFactorList==None:
            return factorList
        factorList=newFactorList

def contractDeltas_termList(termList, *arg, **kw):
    return [contractDeltas_factorList(factorList, *arg, **kw)
            for factorList in termList]


def contractDeltas(exp, *arg, **kw):
    '''cotracts all Deltas as far as possible'''
    termList = lists.makeTermList(exp)
    newTermList = contractDeltas_termList(termList, *arg, **kw)
    return sympy.Add(*[ sympy.Mul(*factorList) for factorList in newTermList ] )


##################### Here be unittest #####################
import unittest

class TestDelta(unittest.TestCase):

    def setUp(self):
        self.t = tensor.Tensor('t')
        self.tf = tensor.TensorFunction('tf')
        self.a = sympy.Dummy('a')
        self.b = sympy.Dummy('b')
        self.c = sympy.Dummy('c')
        self.d = sympy.Dummy('d')
        self.x, self.y, self.z = sympy.symbols('x,y,z')
        self.f = sympy.Function('f')

    def test_ContractDeltas(self):
        t=self.t; tf=self.tf; a=self.a; b=self.b; c=self.c; d=self.d
        x=self.x; y=self.y; z=self.z; f=self.f

        exp = Delta(a,b)*Delta(x,y)*t(b,y)
        self.assertEqual(contractDeltas(exp),t(a,x))

        exp = 13*Delta(a,b)*Delta(b,a)
        self.assertEqual(contractDeltas(exp),13*dim)

        exp = Delta(1,2)*Delta(3,a)*tf(a,3)(x,x)+5
        self.assertEqual(contractDeltas(exp), 5)

        exp = 4711
        self.assertEqual(contractDeltas(exp),4711)

        exp = sympy.diff(Delta(c,a)*tf(a,b)(x,y),y)
        self.assertEqual(contractDeltas(exp),sympy.diff(tf(c,b)(x,y),y))

        exp = tf(x,y)(t(a,b),t(z,z),z)*Delta(y,c)*Delta(a,d) - tf(x,c)(t(d,b),t(z,z),z)
        self.assertEqual(contractDeltas(exp),0)


    def test_dim(self):
        a=self.a
        tempDim=getDim()
        setDim(4)
        self.assertEqual(contractDeltas(Delta(a,a)),4)
        setDim(4711)
        self.assertEqual(contractDeltas(Delta(a,a)),4711)
        self.assertEqual(contractDeltas(Delta(a,a),dim=13) ,13)
        self.assertEqual(contractDeltas(Delta(a,a),indexRange=range(13) ) ,13)
        setDim(tempDim)
        self.assertEqual(getDim(),tempDim)

        

if __name__ == '__main__':
    unittest.main()
