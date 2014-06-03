import unittest

import jsonl
import simplejson as json

class testJSONL_core(unittest.TestCase):
    def setUp(self):
        self.tv = '{"a":1}'
        self.tv1 = '{"a":{"b":2}, "c":3}'
        self.tv_ = {"count":1}
        self.tv1_ = {"a":{"b":2}, "c":[3]}
        self.tvn_ = {'null':1}
        self.tvn1_ = {None:1}
        self.tv2 = {None:1, True:False, 'a':[{'b':'bb', 'c':[1, {'f':'ff', 't':33}]}]}

    def tearDown(self):
        pass

    def testDumpMutableLoad1(self, tv=None):
        tv = tv or self.tv2
        a = jsonl.dumps(tv)
        b = jsonl.loads(a, __mutable__=True)
        c = jsonl.dumps(b)
        assert jsonl.isEqual(json.loads(a), json.loads(c))

    def testDumpImmutableLoad1(self, tv=None):
        tv = tv or self.tv2
        a = jsonl.dumps(tv)
        b = jsonl.loads(a, __mutable__=False)
        c = jsonl.dumps(b)
        assert jsonl.isEqual(json.loads(a), json.loads(c))

    def testCompare(self, tv=None):
        tv = tv or self.tv2
        a = jsonl.dumps(tv)
        for m in [True, False]:
            b = jsonl.loads(a, __mutable__=m)
            d = jsonl.loads(a, __mutable__=m)
            c = jsonl.dumps(b)
            assert jsonl.isEqual(json.loads(a), json.loads(c))
            assert jsonl.isEqual(a, c)
            assert jsonl.isEqual(b, d)
            assert jsonl.isEqual(c, d)

    def testNull(self):
        self.testNone(self.tvn1_)

    def testNone(self, tv=None):
        if tv == None:
            tv = self.tvn1_
        a = jsonl.dumps(tv)
        r = jsonl.loads(a)
        assert r.null == 1

    def testSimpleAttribute(self):
        r = jsonl.loads(self.tv)
        assert r.a == 1

    def testComplexAttribute(self):
        r = jsonl.loads(self.tv1)
        assert r.a.b == 2
        assert r.c == 3

    def testLoadsImmutableNamedTuple(self):
        r = jsonl.loads(self.tv1, __mutable__=False)
        assert r.a.__class__.__name__ == jsonl.OBJECT_NAME
        for i in [r, r.a]:
            try:
                setattr(i, 'test', 1)
            except AttributeError:
                assert True
            else:
                assert False

    def testLoadsMutableObject(self):
        eV = 123
        r = jsonl.loads(self.tv1, __mutable__=True)
        assert r.a.__class__.__name__ == jsonl.OBJECT_NAME
        for i in [r, r.a]:
            try:
                setattr(i, 'test', eV)
            except Exception as _e:
                assert False
            else:
                assert r.test == eV

    def testLoadsMutableObjectByDefault(self):
        r = jsonl.loads(self.tv1)
        assert r.a.__class__.__name__ == jsonl.OBJECT_NAME

    def testDumps(self):
        rd = jsonl.dumps(self.tv_)
        r = jsonl.loads(rd)
        assert r.count == 1

    def testComplexDumps(self):
        rd = jsonl.dumps(self.tv1_)
        r = jsonl.loads(rd)
        assert r.a.__class__.__name__ == jsonl.OBJECT_NAME
        assert r.a.b == 2
        assert r.c == [3]

    def testDumpsEquivelance(self):
        a = json.dumps(self.tv)
        b = jsonl.dumps(self.tv)
        assert a == b

    def testDumpsComplexEquivelance(self):
        assert json.dumps(self.tv1) == jsonl.dumps(self.tv1)

    def testDumpMutableLoad(self, tv=None):
        tv = tv or self.tv
        a = jsonl.dumps(tv)
        b = jsonl.loads(a, __mutable__=True)
        c = jsonl.dumps(b)
        assert a == c

    def testDumpImmutableLoad(self, tv=None):
        tv = tv or self.tv
        a = jsonl.dumps(tv)
        b = jsonl.loads(a, __mutable__=True)
        c = jsonl.dumps(b)
        assert a == c

    def testDumpMutableLoadComplex(self):
        return self.testDumpMutableLoad(tv=self.tv1_)

    def testDumpImmutableLoadComplex(self):
        return self.testDumpImmutableLoad(tv=self.tv1_)

    def getWebEx1(self):
        FN = 'firstName'
        FNV = 'John'
        LN = 'lastName'
        LNV = 'Smith'
        voo = '''{
     "%s": "%s",
     "%s": "%s",
     "age": 25,
     "ageAtBirth": "0",
     "address":
     {
         "streetAddress": "21 2nd Street",
         "city": "New York",
         "state": "NY",
         "postalCode": "10021"
     },
     "phoneNumber":
     [
         {
           "type": "home",
           "number": "212 555-1234"
         },
         {
           "type": "fax",
           "number": "646 555-4567"
         }
     ]
     }''' % (FN, FNV, LN, LNV)
        return (FN, FNV, LN, LNV), voo

    def testWebEx1(self):
        (_FN, FNV, _LN, LNV), voo = self.getWebEx1()
        def check(o):
            assert o.firstName == FNV
            assert o.lastName == LNV
            assert o.age == 25
            assert o.ageAtBirth == "0"
            assert o.address.streetAddress == "21 2nd Street"
            assert o.address.city == "New York"
            assert o.address.state == "NY"
            assert o.address.postalCode == "10021"
            assert o.phoneNumber[0].type == "home"
            assert o.phoneNumber[0].number == "212 555-1234"
            assert o.phoneNumber[1].type == "fax"
            assert o.phoneNumber[1].number == "646 555-4567"
        for m in [True, False]:
            l = jsonl.loads(voo, __mutable__=m)
            check(l)
            d = jsonl.dumps(l)
            assert jsonl.isEqual(l, d)
            for n in [True, False]:
                assert jsonl.isEqual(l, jsonl.loads(d, __mutable__=n))
                assert jsonl.isEqual(d, jsonl.loads(d, __mutable__=n))

    def testDumpMutableTransMutable(self, tv=None, tv2=None):
        tv = tv or self.tv_
        tv2 = tv2 or self.tv2
        a = jsonl.loads(jsonl.dumps(tv), __mutable__=True)
        b = jsonl.loads(jsonl.dumps(tv2), __mutable__=False)
        a.FiElD = b
        try:
            a.FiElD.c = b
        except AttributeError:
            assert True
        else:
            assert False
        c = jsonl.dumps(a)
        d = jsonl.loads(c)
        assert jsonl.isEqual(a, d)
        assert jsonl.isEqual(a, c)

    def testRecursive(self, tv=None):
        tv = tv or self.tv_
        a = jsonl.loads(jsonl.dumps(tv), __mutable__=True)
        #    Make recursive:
        a.FiElD = a
        try:
            jsonl.dumps(a)
        except jsonl.JSONDecodeCircularError:
            assert True
        else:
            assert False

    def testNonRecursive(self, tv=None):
        tv = tv or self.tv_
        a = jsonl.loads(jsonl.dumps(tv), __mutable__=True)
        a1 = jsonl.loads(jsonl.dumps(tv), __mutable__=True)
        #    Make recursive:
        a.FiElD = a1
        jsonl.dumps(a)

    def testRecursiveComplexAllMutable(self):
        _, voo = self.getWebEx1()
        a = jsonl.loads(voo, __mutable__=True)
        a2 = jsonl.loads(voo, __mutable__=True)
        a3 = jsonl.loads(voo, __mutable__=True)
        b = jsonl.loads(jsonl.dumps(self.tv2), __mutable__=False)
        for what in [a, a2, a3]:
            a.FiElD = a2
            a.FiElD.fIeLd = a3
            a.FiElD.fIeLd.fIELd = b
            #    Make recursive:
            a.FiElD.fIeLd.fIELd1 = what
            try:
                jsonl.dumps(a)
            except jsonl.JSONDecodeCircularError:
                assert True
            else:
                assert False

    def testImmutableCannotBeRecursive(self):
        _, voo = self.getWebEx1()
        a = jsonl.loads(voo, __mutable__=True)
        a2 = jsonl.loads(voo, __mutable__=True)
        a3 = jsonl.loads(voo, __mutable__=True)
        b = jsonl.loads(jsonl.dumps(self.tv2), __mutable__=False)
        a.FiElD = a2
        a.FiElD.fIeLd = a3
        #    Make recursive:
        a.FiElD.fIeLd.fIELd = b
        jsonl.dumps(a)

class testJSONL_item(unittest.TestCase):
    def setUp(self):
        self.tv = '{"a":1}'
        self.tv1 = '{"a":{"b":2}, "c":3}'
        self.tv_ = {"count":1}
        self.tv1_ = {"a":{"b":2}, "c":[3]}
        self.tvn_ = {'null':1}
        self.tvn1_ = {None:1}
        self.tv2 = {None:1, True:False, 'a':[{'b':'bb', 'c':[1, {'f':'ff', 't':33}]}]}

    def tearDown(self):
        pass

    def testItemAccess(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        assert obj['null']==1
        assert obj['true']==False
        assert isinstance(obj['a'], list)

    def testItemAccessNotExist(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            obj['doesnotexist']
        except IndexError:
            assert True
        else:
            assert False

    def testItemAssignment(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        obj['y'] = 789
        assert obj['y']==789
        assert obj['true']==False
        obj['true'] = 654
        assert obj['true']==654
 
    def testItemContains(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        assert 'true' in obj
        assert not 'b' in obj
 
    def testItemLength(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        assert len(obj)==3
        assert len(obj['a'])==1
        assert len(obj['a'][0].c)==2
 
    def testItemDeletion(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        assert obj['a']!=None
        del obj['a']
        try:
            obj['a']
        except IndexError:
            assert True
        else:
            assert False
        assert obj['null']==1
        assert obj['true']==False
 
    def testItemDeletionNotExist(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            obj['doesnotexist']
        except IndexError:
            assert True
        else:
            assert False
 
    def testItemAccessInvalidKey(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            obj['_a']
        except KeyError:
            assert True
        else:
            assert False
 
    def testItemAssignmentInvalidKey(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            obj['_a'] = 567
        except KeyError:
            assert True
        else:
            assert False
 
    def testItemDeletionInvalidKey(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            del obj['_a']
        except KeyError:
            assert True
        else:
            assert False

class testJSONL_slice(unittest.TestCase):
    def setUp(self):
        self.tv = '{"a":1}'
        self.tv1 = '{"a":{"b":2}, "c":3}'
        self.tv_ = {"count":1}
        self.tv1_ = {"a":{"b":2}, "c":[3]}
        self.tvn_ = {'null':1}
        self.tvn1_ = {None:1}
        self.tv2 = {None:1, True:False, 'a':[{'b':'bb', 'c':[1, {'f':'ff', 't':33}]}]}

    def tearDown(self):
        pass

    def test(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        assert obj[:]==['a', 'null', 'true']
        assert obj[0:1]==['a']
        assert obj[0:2]==['a', 'null']
        assert obj[0:3]==['a', 'null', 'true']
        assert obj[1:2]==['null']
        assert obj[1:3]==['null', 'true']
        assert obj[2:3]==['true']
        assert obj[-1:-1]==[]
        assert obj[-2:-2]==[]
        assert obj[-3:-3]==[]
        assert obj[-2:-1]==['null']
        assert obj[-3:-1]==['a', 'null']
        assert obj[-3:-2]==['a']
        assert obj[0:4]==['a', 'null', 'true']
        assert obj[1:4]==['null', 'true']
        assert obj[2:4]==['true']
        assert obj[3:4]==[]
        assert obj[4:4]==[]

    def testIndexOutOfRange(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        for stop in xrange(4,10):
            assert obj[4:stop]==[]
        assert obj[-4:-4]==[]
        assert obj[4:4]==[]

class testJSONL_sliceExtendedOperations(unittest.TestCase):
    def setUp(self):
        self.tv = '{"a":1}'
        self.tv1 = '{"a":{"b":2}, "c":3}'
        self.tv_ = {"count":1}
        self.tv1_ = {"a":{"b":2}, "c":[3]}
        self.tvn_ = {'null':1}
        self.tvn1_ = {None:1}
        self.tv2 = {None:1, True:False, 'a':[{'b':'bb', 'c':[1, {'f':'ff', 't':33}]}]}

    def tearDown(self):
        pass

    def testStepCannotBeZero(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            assert obj[::0]==['a', 'null', 'true']
        except ValueError:
            assert True
        else:
            assert False

    def testStep(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        for start in [None, 0]:
            assert obj[start::1]==['a', 'null', 'true']
            assert obj[start::2]==['a', 'true']
            assert obj[start::3]==['a']
            assert obj[start::4]==['a']
        assert obj[1::1]==['null', 'true']
        for stop in xrange(2, 5):
            assert obj[1::stop]==['null']
        for stop in xrange(1, 5):
            assert obj[2::stop]==['true']

    def testStepReversed(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        assert obj[::-1]==['true', 'null', 'a']
        for stop in xrange(5):
            for step in xrange(1, 5):
                assert obj[0:stop:-step]==[]
        assert obj[::-2]==['true', 'a']
        assert obj[::-3]==['true']
        assert obj[::-4]==['true']

    def testInvalidStart(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            obj['1':2] = 3
        except KeyError:
            assert True
        else:
            assert False

    def testInvalidStop(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            obj[1:'2':3]
        except ValueError:
            assert True
        else:
            assert False

    def testInvalidStep(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            obj[1:2:'3']
        except ValueError:
            assert True
        else:
            assert False

class testJSONL_sliceDelExtendedOperations(unittest.TestCase):
    def setUp(self):
        self.tv = '{"a":1}'
        self.tv1 = '{"a":{"b":2}, "c":3}'
        self.tv_ = {"count":1}
        self.tv1_ = {"a":{"b":2}, "c":[3]}
        self.tvn_ = {'null':1}
        self.tvn1_ = {None:1}
        self.tv2 = {None:1, True:False, 'a':[{'b':'bb', 'c':[1, {'f':'ff', 't':33}]}]}

    def tearDown(self):
        pass

#     def testItemAssignment(self):
#         tv = self.tv2
#         obj = jsonl.loads(jsonl.dumps(tv))
#         obj['a':] = [2]
#         assert len(obj)==1
#         assert obj.a==2

    def testDelValidIntegers(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj[0:2:1]
        assert len(obj)==1
        assert obj['true']==False
        assert not 'a' in obj
        assert not 'null' in obj
        
    def testDelValidStrings1(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj['a':'null']
        assert len(obj)==2
        assert obj['null']==1
        assert obj['true']==False
        assert not 'a' in obj

    def testDelValidStrings2(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj['a':'true']
        assert len(obj)==1
        assert not 'a' in obj
        assert not 'null' in obj
        assert 'true' in obj
        
    def testDelValidStrings3(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj['a':'true':1]
        assert len(obj)==1
        assert not 'a' in obj
        assert not 'null' in obj
        assert 'true' in obj
        
    def testDelValidStrings4(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj['a':'true':2]
        assert len(obj)==2
        assert not 'a' in obj
        assert 'null' in obj
        assert 'true' in obj
        
    def testDelValidStrings5(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj['a':'true':-1]
        assert len(obj)==3
        assert 'a' in obj
        assert 'null' in obj
        assert 'true' in obj
        
    def testDelValidReversed(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj[2:0:-1]
        assert len(obj)==1
        assert 'a' in obj
        assert not 'true' in obj
        assert not 'null' in obj

    def testDelValidNoSliceArgs(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        del obj[::]
        assert len(obj)==0

    def testDelInvalidStart(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            del obj['voo':]
        except ValueError:
            assert True
        else:
            assert False

    def testDelInvalidStop(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            del obj[:'voo']
        except ValueError:
            assert True
        else:
            assert False

    def testDelInvalidStartAndStop(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        try:
            del obj['boo':'voo']
        except ValueError:
            assert True
        else:
            assert False

    def testDelInvalidStop(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        for stop in ['s', 'boo', 'voo']:
            try:
                del obj['true':stop]
            except ValueError:
                assert True
            else:
                assert False

    def testDelInvalidStart(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        for start in ['s', 'boo', 'voo']:
            try:
                del obj[start:'true']
            except ValueError:
                assert True
            else:
                assert False

    def testDelInvalidStep(self):
        tv = self.tv2
        obj = jsonl.loads(jsonl.dumps(tv))
        for step in ['', 'true', 'voo']:
            try:
                del obj[0:1:step]
            except ValueError:
                assert True
            else:
                assert False

class testJSONL_iterjson(unittest.TestCase):
    def setUp(self):
        self.tv = '{"a":1}'
        self.tv1 = '{"a":{"b":2}, "c":3}'
        self.tv_ = {"count":1}
        self.tv1_ = {"a":{"b":2}, "c":[3]}
        self.tvn_ = {'null':1}
        self.tvn1_ = {None:1}
        self.tv2 = {None:1, True:False, 'a':[{'b':'bb', 'c':[1, {'f':'ff', 't':33}]}]}
        self.tv3 = [1, 2, {'a':'b'}]

    def tearDown(self):
        pass

    def testString(self):
        tv = self.tv1
        obj = jsonl.loads(tv)
        i = jsonl.iter(obj)
        assert sorted([m for m in i])==['a', 'c']
        i = jsonl.iterkeys(obj)
        assert sorted([m for m in i])==['a', 'c']

    def testDict(self):
        tv = self.tv1_
        i = jsonl.iter(tv)
        assert sorted([m for m in i])==['a', 'c']
        i = jsonl.iterkeys(tv)
        assert sorted([m for m in i])==['a', 'c']

    def testList(self):
        tv = self.tv3
        i = jsonl.iter(tv)
        assert sorted([m for m in i])==tv
        i = jsonl.iterkeys(tv)
        assert sorted([m for m in i])==tv

    def testJsonlObjectTransMutable(self):
        tv = self.tv1
        for m in [True, False]:
            obj = jsonl.loads(tv, __mutable__=m)
            i = jsonl.iter(obj)
            l = sorted([m for m in i])
            assert l==['a', 'c']
            i = jsonl.iterkeys(obj)
            assert sorted([m for m in i])==['a', 'c']

    def testNonJsonlObjectOrString(self):
        tv = self.tv1_
        for f in ['iter', 'iterkeys']:
            i = getattr(jsonl, f)(tv)
            l = sorted([m for m in i])
            assert l==['a', 'c']
        i = jsonl.itervalues(tv)
        l = sorted([m for m in i])
        assert l==[tv['a'], tv['c']]

    def testIterListAsValuesRaisesValueError(self):
        tv = self.tv3
        try:
            jsonl.itervalues(tv)
        except ValueError:
            assert True
        else:
            assert False

    def testIterDictAsValues(self):
        tv = self.tv1_
        i = jsonl.itervalues(tv)
        assert sorted([m for m in i])==[tv['a'], tv['c']]

    def testIterJsonlObjectAsValues(self):
        tv = self.tv1_
        obj = jsonl.loads(jsonl.dumps(tv))
        i = jsonl.itervalues(obj)
        a = sorted([m for m in i])
        for index, ev in enumerate([tv['a'], tv['c']]):
            assert jsonl.isEqual(jsonl.loads(jsonl.dumps(ev)), a[index])

    def testIterItemsOnDict(self):
        tv = self.tv1_
        i = jsonl.iteritems(tv)
        a = sorted([m for m in i])
        aa = sorted([m for m in tv.iteritems()])
        assert a==aa

    def testIterItemsOnListRisesValueError(self):
        tv = self.tv3
        try:
            jsonl.iteritems(tv)
        except ValueError:
            assert True
        else:
            assert False

    def testIterItemsJsonlObject(self):
        tv = self.tv1_
        obj = jsonl.loads(jsonl.dumps(tv))
        i = jsonl.iteritems(obj)
        for k, v in sorted([m for m in i]):
            assert jsonl.isEqual(jsonl.loads(jsonl.dumps(tv[k])), v)

    def testIterItemsNonJsonlObjectOrString(self):
        tv = self.tv1_
        i = jsonl.iteritems(tv)
        a = sorted([m for m in i])
        for k, v in a:
            assert tv[k]==v

if __name__ == '__main__':
    unittest.main()
