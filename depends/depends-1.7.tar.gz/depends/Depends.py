'''
Created on Jun 9, 2014

@author: francis
'''

import itertools

from depends.Errors import DependsError, CircularDependencyError, \
    InvalidDependantName


class depends(object):
    '''
    @summary: The core Depends class.
    '''
    def __init__(self, ref, strict=False):
        '''
        @param ref: The reference for this depends. In strict mode, this
        must start with a character, not a number or underscore.
        @param strict: True = Enable strict mode, False = otherwise.
        @raise InvalidDependantName: 'ref' is invalid if Strict is True.
        '''
        self.__dict__ = {'__strict': strict}
        if strict:
            _checkIsValidRef(ref)
        self.__dict__['__ref'] = ref
        self.__dict__['__satisfied'] = False
        self.__dict__['__parent'] = []    #    if not parent else [parent]
        self._dependencies = {}
    def __delitem__(self, name):
        return self.__del(name)
    def __getitem__(self, name):
        if not isinstance(name, depends):
            name = depends(name)
        return self._dependencies[_Ref(name)]
    def __setitem__(self, name, value):
        if not isinstance(value, depends):
            value = depends(value)
        self._dependencies[name] = value
        _parent(value, self)
    def __setattr__(self, name, value):
        if name in ['__dict__', '_dependencies']:
            return object.__setattr__(self, name, value)
        else:
            if not isinstance(value, depends):
                value = depends(value)
            key = _Ref(getattr(self, name))
            self._dependencies[key] = value
            _parent(value, self)
    def __getattr__(self, name):
        i = [(k, v) for k, v in self._dependencies.items()]
        for k, v in i:
            if name == k:
                return v
        return object.__getattribute__(self.__dict__, name)
    def __delattr__(self, name):
        return self.__del(name)
    def __del(self, name):
        if not isinstance(name, depends):
            name = depends(name)
        try:
            del self._dependencies[_Ref(name)]
        except:
            if _isStrict(self):   raise
    def __add__(self, other):
        if not isinstance(other, list):
            other = [other]
        for (index, item) in enumerate(other):
            if not isinstance(item, depends):
                other[index] = depends(item)
            if _Ref(other[index]) in self._dependencies.keys():
                if _isStrict(self):
                    raise KeyError(_Ref(other[index]))
            else:
                self._dependencies[_Ref(other[index])] = other[index]
                _parent(other[index], self)
                _autoVerify(self)
                _autoVerify(other[index])
        return self
    def __sub__(self, other):
        if not isinstance(other, list):
            other = [other]
        for (index, item) in enumerate(other):
            if not isinstance(item, depends):
                other[index] = depends(item)
            if _Ref(other[index]) not in self._dependencies.keys():
                if _isStrict(self):
                    raise KeyError(_Ref(other[index]))
            else:
                _nparent(self._dependencies[_Ref(other[index])], self)
                del self._dependencies[_Ref(other[index])]
        return self
    def __contains__(self, item):
        if isinstance(item, depends):
            item = _Ref(item)
        x = [i for i in self._dependencies.keys()]
        return item in x
    def __eq__(self, item):
        if verify(self) == verify(item):
            if _Ref(self) == _Ref(item):
                return True
        return False
    def __ne__(self, item):
        return not self == item
    def __iter__(self):
        return iter(self._dependencies.keys())
    def __str__(self):
        return _toString(self, noraise=True)

def dep(a, *args):
    '''
    @summary: Make a depend on b.
    @param a: The item to assign the dependency to.
    @param b: The dependency
    @return: a - allows for nested building: dep(a, dep(b, dep(c, d))).
    @raise exception: KeyError if b not in a and a is STRICT.
    '''
    if not isinstance(a, depends):
        a = depends(a)
    for i in _iterateArgs(args):
        a += i
    return a

def ndep(a, *args):
    '''
    @summary: Make a not depend on b.
    @param a: The item to unassign the dependency from.
    @param b: The dependency
    @return: a.
    @raise exception: KeyError if b not in a and a is STRICT.
    '''
    if not isinstance(a, depends):
        a = depends(a)
    for i in _iterateArgs(args):
        a -= i
    return a

def strict(deps, enabler=True, verify=False, noraise=False, recursive=False):
    '''
    @summary: Make deps STRICT or LAZY
    @param deps: The item to change.
    @param enabler: True = STRICT, FALSE = LAZY.
    @param verify: True = perform explicit verification post set. FALSE = No explicit verification.
    @param noraise: True = Don't raise errors, FALSE = Raise errors if they occur.
    @return: deps.
    @raise exception: CircularDependencyError if applicable.
    '''
    return _setStrict(deps, enabler, verify, noraise, recursive)

def lazy(deps, verify=False, noraise=False, recursive=False):
    '''
    @summary: Make deps LAZY
    @param deps: The item to change.
    @param verify: True = perform explicit verification post set. FALSE = No explicit verification.
    @param noraise: True = Don't raise errors, FALSE = Raise errors if they occur.
    @return: deps.
    @raise exception: CircularDependencyError if applicable.
    '''
    return _setStrict(deps, False, verify, noraise, recursive)

def verify(deps, noraise=False, createRef=None):
    '''
    @summary: Verify deps.
    @param deps: The item to change.
    @param enabler: True = STRICT, FALSE = LAZY.
    @param verify: True = perform explicit verification post set. FALSE = No explicit verification.
    @param noraise: True = Don't raise errors, FALSE = Raise errors if they occur.
    @return: A dictionary containing: {deps.ref:dependencies}.
    @raise exception: CircularDependencyError if applicable.
    '''
    id_ = id(deps)
    d = _walk(deps, [id_, _Ref(deps)], noraise=noraise, createRef=createRef)
    if isinstance(d, basestring):
        return d
    return d[_Ref(deps)]

def flatten(deps, noraise=False):
    '''
    @attention: A generator
    @summary: Flatten the graph yielding lists of ordered dependencies:
                a
                a.b
                a.b.c
                a.b.d
                a.e
                etc...
    '''
    try:
        return _graphPath(_flatten(deps), path=[_Ref(deps)])
    except DependsError as e:
        if noraise is False:
            raise
        return

def _flatten(deps, noraise=False):
    try:
        return verify(deps, noraise=False, createRef=lambda x: x)
    except CircularDependencyError as e:
        if noraise is False:
            raise
        return e

def _graphPath(deps, path):
    yield [path[0]]
    if not isinstance(deps, basestring):
        for i in __graphPath(deps, path):
            yield i

def __graphPath(deps, path):
    def createPath(a, b=None):
        r = [i for i in a]
        if b is not None:
            r.append(b)
        return r
    for i in sorted(deps):
        if not isinstance(i, dict):
            yield createPath(path, i)
        elif isinstance(i, dict):
            for (k, v) in sorted(i.items()):
                path.append(k)
                yield createPath(path)
                for m in __graphPath(v, path):
                    yield m
                path.remove(k)
    pass

def satisfy(deps, *args):
    '''
    @summary: Satisfy the given graph items - all occurances in the entire graph:
    @attention: A generator.
    a.b.c
    a.b.d
    a.c
    '''
    if deps is None:
        raise ValueError('No depends specified')
    if args:
        for item in _iterateArgs(args):
            _satisfy(deps, item)
    else:
        _setSatisfied(deps, enabler=True)

def _iterateArgs(args):
    args = list(args)
    for index, i in enumerate(args):
        if not isinstance(i, list):
            args[index] = [i]
    return list(itertools.chain(*args))

def isSatisfied(*args):
    if args is None:
        raise ValueError('No depends specified')
    return [_isSatisfied(i) for i in _iterateArgs(args)]

def _parent(deps, parent):
    deps.__dict__['__parent'].append(parent)

def _nparent(deps, parent):
    deps.__dict__['__parent'].remove(parent)

def _checkIsValidRef(ref):
    if not isinstance(ref, basestring) or ref.startswith('_'):
        raise InvalidDependantName(ref)

def _toString(deps, depsVisited=None, noraise=False):
    strict = 'STRICT' if _isStrict(deps) else 'LAZY'
    satisfied = 'SATISFIED' if _isSatisfied(deps) else ''
    if strict and satisfied:
        ss = '|'.join([strict, satisfied])
    else:
        ss = strict or satisfied
    s = '(' if ss else ''
    end = ')' if ss else ''

    if depsVisited is None:
        depsVisited = []
    ref = deps.__dict__['__ref']
    try:
        dependencies = []
        sd = ''
        if len(deps._dependencies.items()) == 0:
            sd = '-'
        else:
            for _k, v in sorted(deps._dependencies.items()):
                id_ = id(v)
                ref = _Ref(v)
                if (id_ in depsVisited) or (ref in depsVisited):
                    try:
                        raise CircularDependencyError(ref)
                    except CircularDependencyError as e:
                        if noraise is True:
                            dependencies.append(str(e))
                        else:
                            raise
                else:
                    depsVisited.append(ref)
                    depsVisited.append(id_)
                    dependencies.append(_toString(v, depsVisited, noraise))
                    depsVisited.remove(id_)
                    depsVisited.remove(ref)
            if dependencies:
                sss = []
                for v in dependencies:
                    sss.append(v)
                    sss.append(', ')
                sd = ''.join(sss)
                sd = sd.replace(', ]', ' ]')
        z = ''.join([ss, s, str(_Ref(deps)), ': [', sd, ']', end])
        z = z.replace('[-]', '-')
        z = z.replace('), ])', ')])')
        return z
    except CircularDependencyError as e:
        e.chain.insert(ref)
        raise

def _walk(deps, depsVisited=None, noraise=False, createRef=None):
    def _createRef(ref):
        return {ref: []}
    if createRef is None:
        createRef = _createRef
    if depsVisited is None:
        depsVisited = []
    ref = _Ref(deps)
    try:
        dependencies = []
        result = {ref: dependencies}
        for k, v in sorted(deps._dependencies.items()):
            id_ = id(v)
            ref_ = _Ref(v)
            if (id_ in depsVisited) or (ref_ in depsVisited):
                try:
                    raise CircularDependencyError(ref_)
                except CircularDependencyError as e:
                    if noraise is True:
                        dependencies.append(str(e))
                    else:
                        raise
            else:
                depsVisited.append(id_)
                depsVisited.append(ref_)
                dependencies.append(_walk(v, depsVisited, noraise, createRef))
                depsVisited.remove(id_)
                depsVisited.remove(ref_)
        if len(dependencies) == 0:
            result = createRef(ref)
        return result
    except CircularDependencyError as e:
        e.chain.insert(0, ref)
        raise

def _Ref(deps):
    return deps.__dict__['__ref']

def _isSatisfied(deps):
    return deps.__dict__['__satisfied'] is True

def _setSatisfied(deps, enabler=True):
    deps.__dict__['__satisfied'] = True

def _isStrict(deps):
    return deps.__dict__['__strict']

def _setIsStrict(deps, enabler):
    deps.__dict__['__strict'] = enabler

def _setStrict(deps, enabler, verify_, noraise, recursive):
    depsO = deps
    if deps is None:
        raise ValueError('No depends specified')
    if not isinstance(deps, list):
        deps = [deps]
    for i in deps:
        _setIsStrict(i, enabler)
        if verify_ is True:
            verify(i, noraise=noraise)
    return depsO

def _autoVerify(deps):
    if _isStrict(deps):
        verify(deps)

def _satisfy(deps, item, depsVisited=None, noraise=False):
    if not isinstance(item, depends):
        item = depends(item)
    if depsVisited is None:
        depsVisited = []
    ref = _Ref(deps)
    if ref == _Ref(item):
        _setSatisfied(deps)
    for v in deps._dependencies.values():
        id_ = id(v)
        if isinstance(v, depends):
            ref = _Ref(v)
            if (id_ in depsVisited) or (ref in depsVisited):
                try:
                    raise CircularDependencyError(ref)
                except CircularDependencyError:
                    if noraise is False:
                        raise
            else:
                depsVisited.append(ref)
                depsVisited.append(id_)
                if ref == _Ref(item):
                    _setSatisfied(v)
                _satisfy(v, item, depsVisited, noraise)
                depsVisited.remove(id_)
                depsVisited.remove(ref)

def satisfied(deps):
    '''
    @summary: yield a list of satisfied dependencies
    '''
    for i in _yieldSatisfied(deps, queryStatus=True):
        yield i

def _yieldSatisfied(deps, depsVisited=None, noraise=False, queryStatus=False, ignoreRoot=False):
    '''
    @summary: yield a list of satisfied dependencies
    '''
    if not isinstance(deps, depends):
        deps = depends(deps)
    if depsVisited is None:
        depsVisited = []
    ref = _Ref(deps)
    if _isSatisfied(deps) == queryStatus:
        if ignoreRoot is False:
            yield (ref, deps)
    for v in deps._dependencies.values():
        id_ = id(v)
        if isinstance(v, depends):
            ref = _Ref(v)
            if (id_ in depsVisited) or (ref in depsVisited):
                try:
                    raise CircularDependencyError(ref)
                except CircularDependencyError:
                    if noraise is False:
                        raise
            else:
                depsVisited.append(ref)
                depsVisited.append(id_)
                for i in _yieldSatisfied(v, depsVisited=depsVisited, noraise=noraise, queryStatus=queryStatus, ignoreRoot=False):
                    yield i
                depsVisited.remove(id_)
                depsVisited.remove(ref)

def unsatisfied(deps, ignoreRoot=False):
    '''
    @summary: yield a list of unsatisfied dependencies
    '''
    for i in _yieldSatisfied(deps, queryStatus=False, ignoreRoot=ignoreRoot):
        yield i

def allSatisfied(deps, ignoreRoot=False):
    '''
    @summary: Are all dependencies satisfied?
    '''
    for _ in _yieldSatisfied(deps, queryStatus=False, ignoreRoot=ignoreRoot):
        return False
    return True

def allReady(deps, *args):
    '''
    @summary: Are all the dependencies for a given depends satisfied in the entire tree?
    '''
    if not isinstance(deps, depends):
        deps = depends(deps)
    for _ in unsatisfied(deps, ignoreRoot=True):
        return False
    return True

def ready(deps, noraise=False):
    '''
    @summary: Find all the dependencies for a given depends which themselves
    have satisfied dependencies but which themselves are not satisfied.
    ie: Are ready to be satisfied.
    '''
    a = list(_ready(deps, noraise=noraise))
    return a

def _ready(deps, depsVisited=None, noraise=False, ignoreRoot=False):
    if not isinstance(deps, depends):
        deps = depends(deps)
    if depsVisited is None:
        depsVisited = []
    ref = _Ref(deps)
    #    Are the immediate dependencies satisfied?
    values = deps._dependencies.values()
    if values:
        if all([_isSatisfied(i) for i in values]) is True:
            if not _isSatisfied(deps):
                yield (ref, deps)
        #    Check our children:
        for v in values:
            id_ = id(v)
            if isinstance(v, depends):
                ref = _Ref(v)
                if (id_ in depsVisited) or (ref in depsVisited):
                    try:
                        raise CircularDependencyError(ref)
                    except CircularDependencyError:
                        if noraise is False:
                            raise
                else:
                    depsVisited.append(ref)
                    depsVisited.append(id_)
                    for i in _ready(v, depsVisited=depsVisited, noraise=noraise, ignoreRoot=False):
                        yield i
                    depsVisited.remove(id_)
                    depsVisited.remove(ref)
    else:
        if not _isSatisfied(deps):
            yield (ref, deps)

if __name__ == '__main__':
    d = depends('z', strict=True)
    dep(d, ['a', 'b', 'c'])
    d.a += 'f'
    print [i for i in satisfied(d)]

