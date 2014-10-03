import lists
import sympy
import tensor





def findIndex(exp):
    '''
    Finds all indecis in exp. Returns a dictionary with all idecis found.

    'free': All free indecis, 
            (not to be summed over acording to sumation convention)
    'dummy': All dummy indecis, 
             (too to be summed over acording to sumation convention)
    'tooManny': Indecis that are found to many times, 
                (i.e. more than twise in the same term if index is dummy, 
                 and more than once in the same term if index is free)
    'missingFree': Free indecis that are missing in one or more term.
    'other': indecis that are not of type sympy.Dummy or sympy.Symbol
    '''
    return findIndex_TensorTermList(
        lists.makeTensorTermList(
            lists.makeTermList(exp)))


def findIndex_TensorFactorList(tfl):
    freeIndex = set()
    dummyIndex = set()
    tooMany = set()
    other = set()
    for factor in tfl:
        for ind in factor['indexList']:
            if not tensor.isAllowedDummyIndex(ind):
                other.add(ind)
            elif ind in dummyIndex:
                tooMany.add(ind)
            elif ind in freeIndex:
                freeIndex.remove(ind)
                dummyIndex.add(ind)
            else:
                freeIndex.add(ind)
    return {'free':freeIndex, 
            'dummy':dummyIndex, 
            'tooMany':tooMany,
            'other':other}


def findIndex_TensorTermList(ttl):
    allIndexList = []
    freeIndex = set()
    missingFree = set()
    dummyIndex = set()   
    tooMany = set()
    other = set()    
    for tfl in ttl:
        index = findIndex_TensorFactorList(tfl)
        allIndexList.append(index['free'] | index['dummy'])
        freeIndex |= index['free']
        dummyIndex |= index['dummy']
        tooMany |= index['tooMany']   
        other |= index['other']   
    for allInd in allIndexList:
        missingFree |= (freeIndex - allInd)
    tooMany |= (freeIndex & dummyIndex)
    dummyIndex -= freeIndex 
    return {'free':freeIndex, 
            'dummy':dummyIndex, 
            'tooMany':tooMany,
            'missingFree':missingFree,
            'other':other}





##################### Here be unittest #####################
import unittest

class TestFindIndex(unittest.TestCase):

    def setUp(self):
        self.t = tensor.Tensor('t')
        self.tf = tensor.TensorFunction('tf')
        self.a = sympy.Dummy('a')
        self.b = sympy.Dummy('b')
        self.x, self.y, self.z = sympy.symbols('x,y,z')
        self.f = sympy.Function('f')

    def test_findIndex(self):
        t=self.t; tf=self.tf; a=self.a; b=self.b; 
        x=self.x; y=self.y; z=self.z; f=self.f

        exp = f(t(x), z, tf(x,y)(z, z, tf(z,z)(x,x) ) )
        self.assertEqual(findIndex(exp),{'dummy': {x, z},
                                         'free': {y},
                                         'missingFree': set(),
                                         'other': set(),
                                         'tooMany': set() } )

        exp = t(a,b)+t(a,a)+t(a,b,1)
        self.assertEqual(findIndex(exp),{'dummy': set(),
                                         'free': {b, a},
                                         'missingFree': {b},
                                         'other': {1},
                                         'tooMany': {a} } )

if __name__ == '__main__':
    unittest.main()

