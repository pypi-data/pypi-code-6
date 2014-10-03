import sympy
import tensor

'''
This module re-express mathematicla epressions as lists that are sutible for doing index operations.
lists.py respect comutation relations by always remember the possition of a tensor in the original expression


<!> Always use sympy.expand(exp) before using makeTermList(exp) <!>
If you ignore this recomendation, stuf might not work as expcted.


factorList (fl) is a list of all factors in an expression 

termList (tl) is a list of fl for each arg of a sympy.Add

tensorFactorList (tfl) is always generated from a mother fl. tfl is a list of all tensors (and functions of tensors) that where in the tl. tensorFactors in tfl are represented as list of properties.

tensorTermList (ttl) is always generated from a mother tl. ttl is a list of tfl for each fl in tl.

factor refere to an element in a fl or tfl

tensorFactor refere to an element in a tfl


'''



def makeFactorList(exp):
    if (isinstance(exp,sympy.Pow) 
            and isinstance(exp.args[1],(int,sympy.Integer)) 
            and exp.args[1]>1 ):
        factorList=[]
        base=makeFactorList(exp.args[0])
        for i in range(exp.args[1]):
            factorList.append(base)
        return flatten(factorList)
    if isinstance(exp,sympy.Mul):
        factorList=[]
        for factor in exp.args:
            factorList.append(makeFactorList(factor))
        return flatten(factorList)
    return [exp]
    

def makeTermList(exp):
    if isinstance(exp,sympy.Mul) or isinstance(exp,sympy.Pow):
        return[makeFactorList(exp)]
    if not isinstance(exp,sympy.Add):
        return [[exp]]
    return [makeFactorList(term) for term in exp.args]


def serchIndexInFactor(exp):
    '''
    Find indecis on all levels in an expression.
    indexList is a list of all indecis
    indexDict is a dictionary that maches the possition in indexList with the possiton of that index in the expression.
    '''
    def serch(exp,indexList,indexPos):
        indexDict = {}
        if tensor.isTensor(exp):
            expIndex = []
            for ind in exp.index:
                indexList.append(ind)
                expIndex.append(indexPos)
                indexPos += 1
            indexDict['index'] = expIndex
        if getattr(exp,'args',False):
            argsDict = {}
            for (j,arg) in enumerate(exp.args):
                argDict,indexList,indexPos = serch(arg,indexList,indexPos)
                if argDict: argsDict[j]=argDict     
            if argsDict: indexDict['args']=argsDict         
        return indexDict, indexList, indexPos
    indexList = []; indexPos = 0
    indexDict, indexList, indexPos = serch(exp, indexList, indexPos)
    return indexDict, indexList


def makeTensorFactorList(factorList):
    ret=[]
    for (i,factor) in enumerate(factorList):
        indexDict, indexList = serchIndexInFactor(factor)
        if indexDict:
            tensorFactor={}
            tensorFactor['pos']=i
            tensorFactor['name']=tensor.longTensorName(factor)
            tensorFactor['indexDict']=indexDict
            tensorFactor['indexList']=indexList
            ret.append(tensorFactor)
    return ret


def makeTensorTermList(termList):
    return [makeTensorFactorList(factorList) for factorList in termList]


def rebuildFactor(oldFactor,tensorFactor):
    return withNewIndex(oldFactor, 
                   tensorFactor['indexDict'],
                   tensorFactor['indexList'])


def withNewIndex(factor, indexDict, indexList):
    'Takes an expression, an indexDict as the one created by serchIndexInFactor, and list of (new?) indecis. Builds a new expression, same as factor, but with the indecis in indexList'
    if tensor.isTensor(factor): 
        factor = factor.withNewIndex(
            *[indexList[i] for i in indexDict['index'] ])
    if 'args' in indexDict:
        argsList = list(factor.args)
        argsDict = indexDict['args']
        for (j,arg) in enumerate(argsList):
            if j in argsDict:
                argsList[j] = withNewIndex(arg, argsDict[j], indexList)
        factor = type(factor)(*argsList)
    return factor


def rebuildMul(tensorFactorList,factorList):
    newFactorList = list(factorList)    
    for tensorFactor in tensorFactorList:
        pos = tensorFactor['pos']
        newFactorList[pos] = rebuildFactor(factorList[pos],tensorFactor)
    return sympy.Mul(*newFactorList)


def rebuildAdd(tensorTermList,TermList):
    return sympy.Add(*[rebuildMul(tfl,TermList[i]) 
                       for (i,tfl) in enumerate(tensorTermList)])


def sortTensorTermList(tensorTermList):
    'Organise a ttl in normal form as preparation for module renameInex'
    for tensorFactorList in tensorTermList:
        tensorFactorList.sort(comprTensorsInList)
        

def comprTensorsInList(A,B):
    if A['name'] == B['name']: 
        if indexPathern(A['indexList']) < indexPathern(B['indexList']): 
            return -1
        if indexPathern(A['indexList']) > indexPathern(B['indexList']): 
            return 1
        return 0  
    if A['name'] < B['name']: return -1
    if A['name'] > B['name']: return 1
    return 0

        
def indexPathern(index):
    d = {}
    n = 0
    pathern = []
    for ind in index:
        if not ind in d:
            d[ind] = n
            n = n+1
        pathern.append(d[ind])
    return pathern


def printStructure(exp):
    if getattr(exp, 'args', False):
        return (type(exp).__name__ 
                + "(" 
                + ", ".join([printStructure(arg) for arg in exp.args]) 
                + ")")
    else:
        return str(exp)


def printList(lis):
    l=len(lis)
    if l>2:
        print lis
        return None
    print '[ ' + str(lis[0]) + ' ,'
    for i in range(1,l-1):
        print '  ' + str(lis[i]) + ' ,'
    print '  ' + str(lis[l-1]) + ' ]'
    return None
    

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result
        
