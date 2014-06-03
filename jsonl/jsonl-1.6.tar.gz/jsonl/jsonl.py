from collections import namedtuple
from contextlib import contextmanager
import copy
import traceback
from types import SliceType

import simplejson as __js

_JSONL = 'JSONL'
__version__ = '1.6'
__author__ = 'Francis Horsman'
__email__ = 'francis.horsman@gmail.com'

#    Example configuration (nothing prior to v1.0 is compatible with >= v1.0:
__COMPAT_MATRIX = {'1d6':{'yes':['1d5']},
                   '1d5':{'yes':['1d4']},
                   '1d4':{'yes':['1d3']},
                   '1d3':{'yes':['1d2'], 'no':['0d9', '0d8']},
                   '1d2':{'no':['0d9'], 'yes':['1d0']},
                   '1d0':{'no':['0d9']},
                   '0d9':{},
                   }

class __JSONDecodeCircularError(ValueError):
    def __str__(self):
        return 'Circular dependency: %s' % self.message

class _jsonl(object):
    OBJECT_NAME = '_'.join([_JSONL, 'v1d4'])

_jsonl = _jsonl()

for name in dir(__js):
    setattr(_jsonl, name, getattr(__js, name))

class __baseMutableJson(object):
    '''
    @todo: __setattr__, __getattr__ = Method hooks for future features.
    @note: len = number of attributes (keys) in this json.
    @note: contains = hasattr
    @note: obj[key] notation supported = get, set, del.
    @note: slice[start:stop:step] = slice the json keys from these indexes alphabetically -
        indexes can be a mixture of integer, strings, mutable or immutable jsonl objects -
        note: slice step param must be an integer.
    '''
    def __setattr__(self, name, value):
        return object.__setattr__(self, name, value)
    def __getattribute__(self, name):
        return object.__getattribute__(self, name)
    def __setitem__(self, key, value):
        if isinstance(key, SliceType):
            #    @TODO: Insert and replace all values within slice range.
            raise KeyError(key)
        if not key.startswith('_'):
            return setattr(self, key, value)
        raise KeyError(key)
#         def func(s, k):
#             raise NotImplementedError
#         def func1(s, l, raw=None):
#             print value
#             raise NotImplementedError
#         self.__sliceItem(key, func, func1)
    def __getitem__(self, key):
        return self.__sliceItem(key, lambda s, k: getattr(s, k), lambda s, l, _r: l)
    def __delitem__(self, key):
        return self.__sliceItem(key, lambda s, n: delattr(s, n), lambda s, l, _r: [delattr(s, name) for name in l])
    def __sliceItem(self, key, func, func1):
        if isinstance(key, SliceType):
            l = sorted((n for n in dir(self) if not n.startswith('_')))
            start = key.start
            stop = key.stop
            step = key.step
            if not isinstance(start, int):
                if start is not None and not isinstance(start, int):
                    start = l.index(start)
                else:
                    start = None
            if not isinstance(stop, int):
                if stop is not None and not isinstance(stop, int):
                    stop = l.index(stop)
                else:
                    stop = None
            if step is not None and not isinstance(step, int):
                raise ValueError(step)
            return func1(self, l[start:stop:step], [l, start, stop, step])
        elif isinstance(key, basestring) and not key.startswith('_'):
            if hasattr(self, key):
                return func(self, key)
            else:
                raise IndexError(key)
        raise KeyError(key)
    def __contains__(self, item):
        return hasattr(self, item)
    def __len__(self):
        return len([name for name in dir(self) if not name.startswith('_')])
    def __getslice__(self, i, j):
        return sorted((n for n in dir(self) if not n.startswith('_')))[i:j]

__cls = type(_jsonl.OBJECT_NAME, (__baseMutableJson,), {})()

def __loads(json_data, *args, **kwargs):
    '''
    @see json.loads
    @param kwargs['__mutable__']: True = mutable generic object used, otherwise = immutable collections.namedTuple used.
    '''
    def createImmutable(d):
        attributes, values = zip(*sorted(d.items()))
        return namedtuple(_jsonl.OBJECT_NAME, list(attributes))(*values)
    def createMutable(d):
        cls = copy.deepcopy(__cls)
        for k, v in d.items():
            setattr(cls, k, v)
        return cls
    createCls = createMutable if kwargs.pop('__mutable__', True) else createImmutable
    kwargs['object_hook'] = lambda x: createCls(x)
    return __js.loads(json_data, *args, **kwargs)

def __serializeNode(value, serialized, name):
    if isinstance(value, basestring):
        return value
    @contextmanager
    def checkCirc(value, serialized):
        serialized.append(value)
        yield
        serialized.remove(value)
    #    Circular dependency check:
    if (__cls.__class__ == value.__class__) and (value in serialized):
        raise _jsonl.JSONDecodeCircularError(' '.join([str(value), str(serialized)]))
    #    Now serialize this node:
    if __cls.__class__ == value.__class__:
        with checkCirc(value, serialized):
            value = __serializeMutable(value, serialized)
    elif isinstance(value, list):
        result = []
        for i in value:
            if __cls.__class__ == i.__class__:
                with checkCirc(i, serialized):
                    result.append(__serializeMutable(i, serialized))
            else:
                result.append(i)
        value = result
    elif isinstance(value, dict):
        value = {k: __serializeNode(v, serialized, k) for k, v in value.items()}
    return value

def __serializeMutable(obj, serialized=None):
    if serialized is None:
        serialized = []
    try:
        attributes = obj._asdict().keys()
    except:
        attributes = dir(obj)
    return {name: __serializeNode(getattr(obj, name), serialized, name) for name in attributes if not name.startswith('_')}

def __dumps(obj, *args, **kwargs):
    '''
    @see json.dumps
    @note: Immutable objects serialize already.
    '''
    if not isinstance(obj, basestring):
        if __areClassesCompatable(__cls, obj):
            obj = __serializeMutable(obj)
    return __js.dumps(obj, *args, **kwargs)

def __load(fp, *args, **kwargs):
    if isinstance(fp, basestring):
        return _jsonl.loads(open(fp, 'rb').read().strip(), *args, **kwargs)
    return _jsonl.loads(fp.read().strip(), *args, **kwargs)

def __dump(obj, fp, *args, **kwargs):
    if isinstance(fp, basestring):
        with open(fp, 'wb') as f:
            return f.write(_jsonl.dumps(obj, *args, **kwargs))
    return fp.write(_jsonl.dumps(obj, *args, **kwargs))

def __compare(a, b, force=False):
    '''
    @summary: Comparator method compares persisted values also.
    @param: force: True - force type-coercion.
    @param a: basestring, Any object returned from jsonl.loads()
    @param b: basestring, Any object returned from jsonl.loads()
    '''
    def compare(c, d):
        if type(c) != type(d):    return False
        if isinstance(c, dict):
            #    dicts are order-independent
            attributesC, valuesC = zip(*sorted(c.items()))
            attributesD, valuesD = zip(*sorted(d.items()))
            if not compare(attributesC, attributesD):    return False
            if not compare(valuesC, valuesD):    return False
        elif isinstance(c, (list, tuple)):
            #    lists are order-dependent
            if len(c) != len(d):  return False
            for i in xrange(len(c)):
                if not compare(c[i], d[i]):return False
        return c == d
    aClassName = a.__class__.__name__
    customClassName = __cls.__class__.__name__
    bClassName = b.__class__.__name__
    aIsString = isinstance(a, basestring)
    bIsString = isinstance(b, basestring)
    aIsExactCustomClass = (aClassName == customClassName)
    bIsExactCustomClass = (bClassName == customClassName)
    aIsCustomClass = (aClassName == customClassName)
    bIsCustomClass = (bClassName == customClassName)
    compatable = True
    if aIsCustomClass or bIsCustomClass:
        #    Are our custom classes compatible?
        compatable = __areClassesCompatable(a, b, force)
    if isinstance(a, basestring) and bIsString:
        #    Both are string JSON(l) dumps so compare the actual data:
        return compare(__js.loads(a), __js.loads(b))
    elif aIsExactCustomClass or bIsExactCustomClass:
        if aIsExactCustomClass and bIsExactCustomClass \
            or (aIsCustomClass and bIsCustomClass and compatable):
            #    We have a custom jsonl class as both
            return __compare(__dumps(a), __dumps(b))
        elif aIsExactCustomClass and bIsString:
            #    One custom jsonl class and a string
            return __compare(__dumps(a), b)
        elif bIsExactCustomClass and aIsString:
            #    One custom jsonl class and a string
            return __compare(a, __dumps(b))
    return compare(a, b)

def __areClassesCompatable(a, b, force=False):
    '''
    @note: At least one of a or b is a custom class.
    Both classes must be compatable with 'this' version.
    '''
    if force:   return True
    aClassName = a.__class__.__name__
    customClassName = __cls.__class__.__name__
    bClassName = b.__class__.__name__
    if not aClassName.startswith(_JSONL):   return False
    if aClassName == bClassName:  return True
    aIsCustomClass = (aClassName == customClassName)
    bIsCustomClass = (bClassName == customClassName)
    if (aIsCustomClass and not bIsCustomClass) or\
        (bIsCustomClass and not aIsCustomClass):
        return False
    #    Both are guaranteed to be custom classes at this point.
    tokensCurrent = _jsonl.OBJECT_NAME.split('_')
    tokensA = a.__class__.__name__.split('_')
    tokensB = b.__class__.__name__.split('_')
    versionCurrent = tokensCurrent[1]
    versionA = tokensA[1]
    versionB = tokensB[1]
    #    Check the classes dependency graphs for (in)compatibility
    return __checkCompatibility(versionA, versionCurrent) and __checkCompatibility(versionB, versionCurrent)

def __checkCompatibility(a, versionCurrent):
    '''
    @note: 'a'!=versionCurrent. If 'a' > 'versionCurrent' then False,
    if 'a' not in matrix-tree then assume False.
    @todo: Refactor this out into a separate class.
    '''
    #    Is a compatible with versionCurrent or vici versa?
    try:
        splitter = 'd'
        version = 'v'
        vString = a[1:]
        vcString = versionCurrent[1:]
        tokensA = vString.split(splitter)
        if a[0] != version: raise __JsonlParseError(a, versionCurrent)
        if versionCurrent[0] != version: raise __JsonlParseError(a, versionCurrent)
        tokensV = vcString.split(splitter)
        def greaterThan(c, d):
            if c[0] > d[0]: return True
            if d[0] > c[0]: return False
            if c[1] > d[1]: return True
            return False
        def find(a, versionCurrent, matrix):
            '''
            @note: 'a' is guaranteed to be < versionCurrent
            '''
            if a not in matrix.keys():  return False
            if versionCurrent not in matrix.keys():
                raise __JsonlParseError(a, versionCurrent)
            def get(a, node, visited):
                yes = node.get('yes', [])
                no = node.get('no', [])
                if a in no:
                    raise __No()
                elif a in yes:
                    raise __Yes()
                #    Recurse - explicit 'yes' is required:
                for i in yes:
                    #    Check for circular dependency:
                    if i in visited:
                        raise __Circ(''.join([version, i]))
                    if i in matrix:
                        get(a, matrix[i], set(list(visited) + [i]))
            try:
                get(a, matrix[versionCurrent], set([]))
            except __Yes:
                return True
            except __No:
                return False
            except __Circ:
                raise
            #    Explicit Failure if we can't find it!
            return False
        #    Check a>v:
        if greaterThan(tokensA, tokensV):   return False
        if not find(vString, vcString, __COMPAT_MATRIX): return False
        return True
    except __JsonlParseError as e:
        e.traceback = traceback.format_exc()
    except Exception as e:
        raise __JsonlParseError(a, versionCurrent, e, traceback.format_exc())

class __Yes(Exception):   pass
class __No(Exception):    pass
class __Circ(Exception):
    def __str__(self):
        return 'Circular dependency: %s' % self.message

class __JsonlParseError(Exception):
    def __init__(self, a, versionCurrent, e=None, trace=None):
        self.traceback = trace
        self.version = a
        self.versionCurrent = versionCurrent
        super(__JsonlParseError, self).__init__(e)
    def __str__(self):
        s = [str(self.args[0]), 'in', self.version]
        if self.traceback != None:
            s.append('\n')
            s.append(self.traceback)
        return ' '.join(s)

def __newIterjson(cls, areClassesCompatable):
    class __baseIterator(object):
        @staticmethod
        def _getAttributes(obj):
            try:
                attributes = obj._asdict().keys()
            except:
                attributes = dir(obj)
            return attributes
        def __iter__(self):
            return self._iter
    class __iteratorKeys(__baseIterator):
        def __init__(self, obj):
            if isinstance(obj, basestring):
                obj = _jsonl.loads(obj)
            if self._areClassesCompatable(obj, self._clazz):
                self._iter = iter(sorted((n for n in self._getAttributes(obj) if not n.startswith('_'))))
            else:
                self._iter = iter(obj)
    class __iteratorValues(__baseIterator):
        def __init__(self, obj):
            if isinstance(obj, basestring):
                obj = _jsonl.loads(obj)
            if self._areClassesCompatable(obj, self._clazz):
                self._iter = iter(sorted((obj[n] for n in self._getAttributes(obj) if not n.startswith('_'))))
            elif isinstance(obj, dict):
                self._iter = iter(obj.values())
            elif isinstance(obj, list):
                raise ValueError(obj)
            else:
                self._iter = iter(obj)
    class __iteratorItems(__baseIterator):
        def __init__(self, obj):
            if isinstance(obj, basestring):
                obj = _jsonl.loads(obj)
            if self._areClassesCompatable(obj, self._clazz):
                self._iter = iter([(n, obj[n]) for n in self._getAttributes(obj) if not n.startswith('_')])
            elif isinstance(obj, dict):
                self._iter = iter(sorted(obj.items()))
            else:
                raise ValueError(obj)
    __baseIterator._clazz = cls
    __baseIterator._areClassesCompatable = staticmethod(areClassesCompatable)
    return __iteratorKeys, __iteratorValues, __iteratorItems
__iterKeys, __iterValues, __iterItems = __newIterjson(__cls, __areClassesCompatable)
__iterjson = __iterKeys

setattr(_jsonl, 'load', __load)
setattr(_jsonl, 'loads', __loads)
setattr(_jsonl, 'dump', __dump)
setattr(_jsonl, 'dumps', __dumps)
setattr(_jsonl, 'isEqual', __compare)
setattr(_jsonl, '__version__', __version__)
setattr(_jsonl, '__author__', __author__)
setattr(_jsonl, '__email__', __email__)
setattr(_jsonl, 'JSONDecodeCircularError', __JSONDecodeCircularError)
setattr(_jsonl, 'iter', __iterjson)
setattr(_jsonl, 'iterkeys', __iterKeys)
setattr(_jsonl, 'itervalues', __iterValues)
setattr(_jsonl, 'iteritems', __iterItems)

#    Check the version string:
__tokens = _jsonl.OBJECT_NAME.split('_')
if __tokens[0] != _JSONL:
    raise Exception('JSONL version incorrectly formatted: "%s"' % _jsonl.OBJECT_NAME)
elif __tokens[1][1:] not in __COMPAT_MATRIX.keys():
    raise Exception('Current JSONL version not in compatibility matrix: "%s"' % _jsonl.OBJECT_NAME)
#    TODO:    Perform static circular dependency check and logic check of __COMPAT_MATRIX.

if __name__ == '__main__':
    pass
