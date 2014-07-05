'''
Created on Jun 9, 2014

@author: francis
'''

import unittest

from depends import depends, verify, flatten, dep, ndep, strict, isSatisfied, satisfy, lazy, CircularDependencyError, InvalidDependantName, satisfied, allSatisfied, unsatisfied, allReady, ready

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNestedDep(self):
        b = depends('b')
        a = dep(depends('a'), dep(b, 'c'))
        print a.b
        print b
        assert a.b == b
        del a.b.c
        print a

    def testInvalidRefNone(self):
        try:
            depends(None, strict=True)
        except InvalidDependantName as e:
            assert e.message == None

    def testInvalidRefNonString(self):
        for i in [123, True, False, (1,), [], {}]:
            try:
                depends(i, strict=True)
            except InvalidDependantName as e:
                assert e.message == i

    def testInvalidRefStartsWithUnderscore(self):
        for i in ['_123', '_abc', '__ytr']:
            try:
                depends(i, strict=True)
            except InvalidDependantName as e:
                assert e.message == i

    def testValidRefIsBasestring(self):
        for i in ['hello.world', u'hello.world']:
            try:
                depends(i, strict=True)
            except InvalidDependantName as e:
                assert e.message == i

    def testToggleStrict(self):
        d = depends('z', strict=True)
        strict(d, False)
        strict(d, True)

    def testChangeStrict(self):
        d = depends('z', strict=True)
        lazy(d)
        strict(d, True)

    def testStrict(self):
        d = depends('voo', strict=True)
        d += 'b'
        assert 'b' in d
        d.b += 'c'
        assert 'c' in d.b
        assert 'c' not in d
        for i in d:
            assert i in ['b']
        try:
            d += 'b'
        except KeyError:
            assert True
        else:
            assert False
        try:
            dep(d, 'b')
        except KeyError:
            assert True
        else:
            assert False
        d -= 'b'
        try:
            d -= 'b'
        except KeyError:
            assert True
        else:
            assert False
        try:
            ndep(d, 'b')
        except KeyError:
            assert True
        else:
            assert False
        d += 'b'
        ndep(d, 'b')
        assert 'b' not in d

    def testNonStrict(self):
        d = depends('z', strict=False)
        d += 'b'
        assert 'b' in d
        d.b += 'c'
        assert 'c' in d.b
        assert 'c' not in d
        for i in d:
            assert i in ['b']
        d += 'b'
        dep(d, 'b')
        d -= 'b'
        d -= 'b'
        ndep(d, 'b')
        d += 'b'
        ndep(d, 'b')
        assert 'b' not in d

    def testVerify(self):
        d = depends('z')
        assert not verify(d)

    def testAddRependz(self):
        d0 = depends('z', strict=False)
        d1 = depends('y', strict=False)
        d2 = depends('x', strict=False)
        d3 = depends('w', strict=False)
        d4 = depends('v', strict=False)
        d1 += d2
        d2 += d3
        d2 += d1
        d1 += d0
        print ':', d1
        d0 += d4
        print d0

class TestWalk(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNoDependencies(self):
        d0 = depends(0, strict=False)
        assert not verify(d0)

    def testSimpleDependencies(self):
        d0 = depends('y', strict=False)
        d1 = depends('z', strict=False)
        dep(d0, 'c')
        dep(d0.c, 'f')
        d0 += 'd'
        verify(d0)
        dep(d0, d1)
        dep(d0.c.f, d0)
        try:
            verify(d0, False)
        except CircularDependencyError as e:
            print e
            assert str(e) == 'CIRC(y.c.f.y)'
        else:
            assert False
        assert verify(d0, True)[0]['c'][0]['f'][0] == 'CIRC(y)'
        ss = str(d0)
        assert ss.count('CIRC') == 1
        return (d0, d1)

    def testSTRNoCirc(self):
        (d0, _d1) = self.testSimpleDependencies()
        print d0
        d0.c.f -= 'y'
        assert str(d0).count('CIRC') == 0

    def testSTRWithCirc(self):
        (d0, d1) = self.testSimpleDependencies()
        assert str(d0).count('CIRC') == 1
        assert str(d1).count('CIRC') == 0

    def testStrictCombos(self):
        for a, b, c in [(False, True, 'z'), (True, False , 'y'), (True, True, 'z')]:
            print a, b
            d0 = depends('y', strict=a)
            d1 = depends('z', strict=b)
            assert not verify(d0)
            assert not verify(d1)
            dep(d0, d1)
            try:
                dep(d0.z, d0)
            except CircularDependencyError as e:
                assert e.message == c
            else:
                assert False

    def testStrictVerifiesNoRaise(self):
        d0 = depends('y', strict=True)
        d1 = depends('z', strict=False)
        dep(d0, d1)
        strict(d0, enabler=False)
        dep(d1, d0)
        s = strict(d0, enabler=True, verify=True, noraise=True)
        assert str(s).count('CIRC') == 1
        strict(d0, enabler=False)

    def testStrictVerifiesRaise(self):
        d0 = depends('y', strict=True)
        d1 = depends('z', strict=False)
        dep(d0, d1)
        strict(d0, enabler=False)
        dep(d1, d0)
        try:
            strict(d0, enabler=True, verify=True, noraise=False)
        except CircularDependencyError as e:
            assert e.message == 'y'
        else:
            assert False

    def testEquality(self):
        a = depends('hashable_a', strict=False)
        b = depends('hashable_b', strict=False)
        assert a != b
        c = depends('hashable_b', strict=False)
        assert b == c

    def testIteration(self):
        a = depends('a', strict=False)
        a += 'b'
        a += 'c'
        print [i for i in a]

    def testGetItemValid(self):
        a = depends('a', strict=False)
        a + 'b'
        a.b = 'c'
        assert a['b'] == a.b

    def testGetItemInvalid(self):
        a = depends('a', strict=False)
        try:
            a['b']
        except KeyError as e:
            assert e.message == 'b'
        else:
            assert False
        try:
            a.b
        except AttributeError as e:
            assert True
        else:
            assert False

    def testDelAttr(self):
        a = depends('a', strict=False)
        del a.b

    def testDelAttrStrict(self):
        a = depends('a', strict=True)
        try:
            del a.b
        except KeyError as e:
            assert e.message == 'b'
        else:
            assert False

    def testDelItem(self):
        a = depends('a', strict=False)
        del a['b']

    def testDelItemStrict(self):
        a = depends('a', strict=True)
        try:
            del a['b']
        except KeyError as e:
            assert e.message == 'b'
        else:
            assert False

    def testSatisfy(self):
        a = depends('a', strict=True)
        b = depends('b', strict=True)
        c = depends('c', strict=True)
        d = depends('d', strict=True)
        a += b
        a += c
        a.b = d
        a.c = d
        print a
        satisfy(a, d)
        print a
        print a

class TestPrintStrict(unittest.TestCase):
    def setUp(self, strict=True, eName='STRICT'):
        self._strict = strict
        self._eName = eName

    def tearDown(self):
        pass

    def testNoDeps(self):
        d = depends('z', strict=self._strict)
        s = str(d)
        assert s == "?(z: -)".replace('?', self._eName)

    def testSingle(self):
        d = depends('z', strict=self._strict)
        d += 'a'
        s = str(d)
        assert s == "?(z: [LAZY(a: -)])".replace('?', self._eName)

    def testMultipleSingleDepth(self):
        d = depends('z', strict=self._strict)
        d += 'a'
        d += ['c', 'b', 'd']
        s = str(d)
        assert s == '?(z: [LAZY(a: -), LAZY(b: -), LAZY(c: -), LAZY(d: -)])'.replace('?', self._eName)

    def testSingleMultipleDepth(self):
        d = depends('z', strict=self._strict)
        d += 'a'
        d.a += ['c']
        s = str(d)
        assert s == "?(z: [LAZY(a: [LAZY(c: -)])])".replace('?', self._eName)

    def testSingleMultipleDepth1(self):
        d = depends('z', strict=self._strict)
        d += 'a'
        d.a += ['c']
        d.a.c += ['d']
        s = str(d)
        assert s == "?(z: [LAZY(a: [LAZY(c: [LAZY(d: -)])])])".replace('?', self._eName)

    def testMultipleMultipleDepth(self):
        d = depends('z', strict=self._strict)
        d += 'a'
        d.a += ['c']
        d.a.c += ['d']
        d += 'f'
        d += 'l'
        d.a += ['g']
        d.a += ['k']
        d.a.c += ['h']
        d.a.c += ['i']
        s = str(d)
        print s
        assert s == "?(z: [LAZY(a: [LAZY(c: [LAZY(d: -), LAZY(h: -), LAZY(i: -)]), LAZY(g: -), LAZY(k: -)]), LAZY(f: -), LAZY(l: -)])".replace('?', self._eName)

class TestPrintLazy(TestPrintStrict):
    def setUp(self, strict=False, eName='LAZY'):
        return TestPrintStrict.setUp(self, strict=strict, eName=eName)

class TestSatisfy(unittest.TestCase):
    def setUp(self, strict=True, eName='STRICT'):
        self._strict = strict
        self._eName = eName

    def testSingleDepth(self):
        d = depends('z', strict=self._strict)
        dep(d, ['a', 'b', 'c'], 'd', 'f')
        for i in ['a', 'c']:
            satisfy(d, i)
        assert isSatisfied(d.a) == [True]
        assert isSatisfied(d.c) == [True]
        assert isSatisfied(d) == [False]
        assert isSatisfied(d.b) == [False]
        assert isSatisfied(d.f) == [False]
        assert isSatisfied(d.d) == [False]

    def testMultipleDepth(self):
        d = depends('z', strict=self._strict)
        dep(d, ['a', 'b', 'c'], 'd', 'f')
        dep(d.a, 'y', 'z')
        dep(d.a.y, 'q')
        for i in ['c', 'q']:
            satisfy(d, i)
        assert isSatisfied(d.c) == [True]
        assert isSatisfied(d.a.y.q) == [True]
        assert isSatisfied(d.a.y) == [False]
        assert isSatisfied(d.a) == [False]
        assert isSatisfied(d.b) == [False]
        assert isSatisfied(d.d) == [False]
        assert isSatisfied(d.f) == [False]

class TestFlatten(unittest.TestCase):
    def setUp(self, strict=True, eName='STRICT'):
        self._strict = strict
        self._eName = eName

    def testSingleDepth(self):
        d = depends('z', strict=self._strict)
        dep(d, ['a', 'b', 'c'], 'd', 'f')
        for i in ['a', 'c']:
            satisfy(d, i)
        i = list(flatten(d))
        assert len(i) == 6
        assert i[0] == ['z']
        assert i[1] == ['z', 'a']
        assert i[2] == ['z', 'b']
        assert i[3] == ['z', 'c']
        assert i[4] == ['z', 'd']
        assert i[5] == ['z', 'f']

    def testMultipleDepth(self):
        d = depends('z', strict=self._strict)
        dep(d, ['a', 'b', 'c'], 'd', 'f')
        dep(d.a, 'y', 'w')
        dep(d.a.y, 'q')
        i = list(flatten(d))
        assert len(i) == 9
        assert i[0] == ['z']
        assert i[1] == ['z', 'a']
        assert i[2] == ['z', 'a', 'y']
        assert i[3] == ['z', 'a', 'y', 'q']
        assert i[4] == ['z', 'a', 'w']
        assert i[5] == ['z', 'b']
        assert i[6] == ['z', 'c']
        assert i[7] == ['z', 'd']
        assert i[8] == ['z', 'f']

    def testGraphPathNoDepth(self):
        d = depends('z', strict=self._strict)
        i = list(flatten(d))
        assert len(i) == 1
        assert i[0] == ['z']

    def testGraphPathSingleDepth(self):
        d = depends('z', strict=self._strict)
        dep(d, ['a', 'b', 'c'], 'd', 'f')
        i = list(flatten(d))
        assert len(i) == 6
        assert i[0] == ['z']
        assert i[1] == ['z', 'a']
        assert i[2] == ['z', 'b']
        assert i[3] == ['z', 'c']
        assert i[4] == ['z', 'd']
        assert i[5] == ['z', 'f']

    def testGraphPathMultipleDepth(self):
        d = depends('z', strict=self._strict)
        dep(d, ['a', 'b', 'c'])
        d.a += 'f'
        i = list(flatten(d))
        assert len(i) == 5
        assert i[0] == ['z']
        assert i[1] == ['z', 'a']
        assert i[2] == ['z', 'a', 'f']
        assert i[3] == ['z', 'b']
        assert i[4] == ['z', 'c']
        d.a += ['g', 'q']
        d.b += [dep('h', ['i', 'j']), 'k']
        i = list(flatten(d))
        assert len(i) == 11
        assert i[0] == ['z']
        assert i[1] == ['z', 'a']
        assert i[2] == ['z', 'a', 'f']
        assert i[3] == ['z', 'a', 'g']
        assert i[4] == ['z', 'a', 'q']
        assert i[5] == ['z', 'b']
        assert i[6] == ['z', 'b', 'h']
        assert i[7] == ['z', 'b', 'h', 'i']
        assert i[8] == ['z', 'b', 'h', 'j']
        assert i[9] == ['z', 'b', 'k']
        assert i[10] == ['z', 'c']

    def testGraphPathWithCircularDependency(self):
        d = depends('z', strict=False)
        dep(d, 'a')
        d.a += d
        try:
            verify(d)
        except CircularDependencyError:
            assert True
        else:
            assert False
        try:
            list(flatten(d))
        except CircularDependencyError:
            assert True
        else:
            assert False

class TestSatisfied(unittest.TestCase):
    def setUp(self, strict=True, eName='STRICT'):
        self._strict = strict
        self._eName = eName
        self._d = depends('z', strict=self._strict)
        dep(self._d, ['a', 'b', 'c'])
        self._d.a += 'f'

    def testNothingIsSatisfied(self):
        satisfiedValues = [i for i in satisfied(self._d)]
        assert len(satisfiedValues) == 0

    def testSatisfiedAtDepthZero(self):
        satisfy(self._d, 'z')
        satisfiedValues = [i for i in satisfied(self._d)]
        assert len(satisfiedValues) == 1
        assert satisfiedValues[0][0] == 'z'
        assert isinstance(satisfiedValues[0][1], depends)

    def testSatisfiedAtDepthOne(self):
        satisfy(self._d, 'a')
        satisfiedValues = [i for i in satisfied(self._d)]
        assert len(satisfiedValues) == 1
        assert satisfiedValues[0][0] == 'a'
        assert isinstance(satisfiedValues[0][1], depends)
        satisfy(self._d, 'b', 'c')
        satisfiedValues = [i for i in satisfied(self._d)]
        assert len(satisfiedValues) == 3
        assert 'b' in [satisfiedValues[1][0], satisfiedValues[2][0]]
        assert 'c' in [satisfiedValues[1][0], satisfiedValues[2][0]]
        assert isinstance(satisfiedValues[1][1], depends)
        assert isinstance(satisfiedValues[2][1], depends)

    def testSatisfiedAtDepthTwo(self):
        assert len(list(unsatisfied(self._d))) == 5
        satisfy(self._d, 'f')
        assert len(list(unsatisfied(self._d))) == 4
        satisfiedValues = [i for i in satisfied(self._d)]
        assert len(satisfiedValues) == 1
        assert satisfiedValues[0][0] == 'f'
        assert isinstance(satisfiedValues[0][1], depends)

    def testAllSatisfied(self):
        assert len(list(unsatisfied(self._d))) == 5
        satisfy(self._d, 'a')
        assert not allSatisfied(self._d)
        assert len(list(unsatisfied(self._d))) == 4
        satisfy(self._d, ['b', 'c'], 'f')
        assert not allSatisfied(self._d)
        assert len(list(unsatisfied(self._d))) == 1
        satisfy(self._d, 'z')
        assert allSatisfied(self._d)
        assert len(list(unsatisfied(self._d))) == 0

    def testSatisfiedDependencies(self):
        assert not allReady(self._d)
        satisfy(self._d, ['a', 'b'])
        assert not allReady(self._d)
        satisfy(self._d, ['a', 'b'], 'c')
        assert not allReady(self._d)
        satisfy(self._d, 'f')
        assert allReady(self._d)

    def testAllSatisfiedDependencies(self):
        d = depends('a', strict=True)
        asd = ready(d)
        assert len(asd) == 1

        satisfy(d)
        asd = ready(d)
        assert len(asd) == 0

        d = depends('a', strict=True)
        dep(d, 'b')
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['b']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d, 'b')
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['a']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d)
        asd = ready(d)
        eLen = 0
        assert len(asd) == eLen
        for i in []:
            assert i in [asd[k][0] for k in xrange(eLen)]

        d = depends('a', strict=True)
        dep(d, 'b')
        satisfy(d, 'a')
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['b']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d, 'b')
        asd = ready(d)
        eLen = 0
        assert len(asd) == eLen
        for i in []:
            assert i in [asd[k][0] for k in xrange(eLen)]

        d = depends('a', strict=True)
        dep(d, 'b')
        satisfy(d.b)
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['a']:
            assert i in [asd[k][0] for k in xrange(eLen)]

    def testAllSatisfiedDependenciesComplex(self):
        d = depends('a', strict=True)
        dep(d, ['b', 'o'])
        dep(d.b, 'c', 'g')
        dep(d.b.c, 'd', 'e')
        dep(d.b.g, 'h', 'n')
        dep(d.b.g.h, 'i', 'j', 'l', 'm')
        dep(d.b.g.h.j, 'k')
        dep(d.o, 'p', 'q')
        satisfy(d, 'c', 'd', 'e', 'i', 'k', 'l', 'm', 'o', 'p')
        asd = ready(d)
        eLen = 3
        assert len(asd) == eLen
        for i in ['j', 'n', 'q']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d.o, 'q')
        asd = ready(d)
        eLen = 2
        assert len(asd) == eLen
        for i in ['j', 'n']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d.b.g.h.j)
        asd = ready(d)
        eLen = 2
        assert len(asd) == eLen
        for i in ['h', 'n']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d.b.g.h)
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['n']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d.b.g.n)
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['g']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d.b.g.n)
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['g']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d.b.g)
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['b']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        satisfy(d.b)
        asd = ready(d)
        eLen = 1
        assert len(asd) == eLen
        for i in ['a']:
            assert i in [asd[k][0] for k in xrange(eLen)]

        u = list(unsatisfied(d))
        eLen = 1
        assert len(u) == eLen
        for i in ['a']:
            assert i in [u[k][0] for k in xrange(eLen)]

        satisfy(d)
        u = list(unsatisfied(d))
        eLen = 0
        assert len(u) == eLen


if __name__ == "__main__":
    unittest.main()
