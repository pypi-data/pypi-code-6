# -*- coding: utf-8 -*-

''' Multimethods

An implementation of multimethods for Python, heavily influenced by
the Clojure programming language.

Copyright (C) 2010-2011 by Daniel Werner.

Improvements by Jeff Weiss and others.

See the README file for information on usage and redistribution.
'''

import sys
py_major_version = sys.version_info[0]
if py_major_version >= 3:
    _type_classes = (type,)
else:
    import types
    _type_classes = (type, types.ClassType)

# only if not already defined, prevents mismatch when reloading modules
if 'Default' not in globals():
    class DefaultMethod(object):
        def __repr__(self):
            return '<DefaultMethod>'

    Default = DefaultMethod()


if 'Anything' not in globals():
    class AnythingType(object):
        def __repr__(self):
            return '<Anything>'

    Anything = AnythingType()


def _parents(x):
    return (hasattr(x, '__bases__') and x.__bases__) or ()


def type_dispatch(*args, **kwargs):
    return tuple(type(x) for x in args)


def single_type_dispatch(*args, **kwargs):
    return type(args[0])


class DispatchException(Exception):
    pass


class MultiMethod(object):

    def __init__(self, name, dispatchfn):
        if not callable(dispatchfn):
            raise TypeError('dispatch function must be a callable')

        self.dispatchfn = dispatchfn
        self.methods = {}
        self.preferences = {}
        self.cache = {}
        self.__name__ = name
        # self.cache_hites

    def __call__(self, *args, **kwds):
        dv = self.dispatchfn(*args, **kwds)
        best = self.get_method(dv)
        return best(*args, **kwds)

    def add_method(self, dispatchval, func):
        self.methods[dispatchval] = func
        self._reset_cache()

    def remove_method(self, dispatchval):
        del self.methods[dispatchval]
        self._reset_cache()

    def get_method(self, dv):
        target = self.cache.get(dv, None)
        if target:
            return target
        k = self.find_best_method(dv)
        if k is not Default or k in self.methods:
            target = self.methods[k]
            self.cache[dv] = target
            return target
        if target:
            return target
        else:
            raise DispatchException("No matching method on multimethod '%s' for '%s', and "
                                    "no default method defined" % (self.__name__, dv))

    def _reset_cache(self):
        self.cache = self.methods.copy()

    def _dominates(self, x, y):
        return self._prefers(x, y) or _is_a(x, y)

    def find_best_method(self, dv):
        best = Default
        for k in self.methods:
            if k is Default:
                continue  # don't bother comparing with Default
            if _is_a(dv, k):
                if best is Default or self._dominates(k, best):
                    best = k
                # raise if there's multiple matches and they don't point
                # to the exact same method
                if (not self._dominates(best, k)) and \
                   (self.methods[best] is not self.methods[k]):
                    raise DispatchException("Multiple methods in multimethod '%s'"
                                            " match dispatch value %s -> %s and %s, and neither is"
                                            " preferred" % (self.__name__, dv, k, best))
        # self.cache[dv] = best
        # print self.cache
        # print self.methods
        return best

    def _prefers(self, x, y):
        xprefs = self.preferences.get(x)
        if xprefs is not None and y in xprefs:
            return True
        for p in _parents(y):
            if self._prefers(x, p):
                return True
        for p in _parents(x):
            if self._prefers(p, y):
                return True
        return False

    def prefer(self, dispatchvalX, dispatchvalY):
        if self._prefers(dispatchvalY, dispatchvalX):
            raise Exception("Preference conflict in multimethod '%s':"
                            " %s is already preferred to %s" %
                            (self.__name__, dispatchvalY, dispatchvalX))
        else:
            cur = self.preferences.get(dispatchvalX, set())
            cur.add(dispatchvalY)
            self.preferences[dispatchvalX] = cur
            self._reset_cache()

    def method(self, dispatchval):
        def method_decorator(func):
            self.add_method(dispatchval, func)
            return func
        return method_decorator

    def __repr__(self):
        return "<MultiMethod '%s'>" % _name(self)


def _name(f):
    return "%s.%s" % (f.__module__, f.__name__)


def _copy_attrs(source, dest):
    dest.__doc__ = source.__doc__
    dest.__module__ = source.__module__


def multimethod(dispatch_func):
    '''Create a multimethod that dispatches on the given dispatch_func,
    and uses the given default_func as the default dispatch.  The
    multimethod's descriptive name will also be taken from the
    default_func (its module and name).

    '''
    def multi_decorator(default_func):
        m = MultiMethod(default_func.__name__, dispatch_func)
        m.add_method(Default, default_func)
        _copy_attrs(default_func, m)
        return m
    return multi_decorator


def singledispatch(default_func):
    '''Like python 3.4's singledispatch. Create a multimethod that
    does single dispatch by the type of the first argument. The
    wrapped function will be the default dispatch.
    '''
    m = MultiMethod(default_func.__name__, single_type_dispatch)
    m.add_method(Default, default_func)
    _copy_attrs(default_func, m)
    return m


def multidispatch(default_func):
    '''Create a multimethod that does multiple dispatch by the types of
    all the arguments. The wrapped function will be the default
    dispatch.

    '''
    m = MultiMethod(default_func.__name__, type_dispatch)
    m.add_method(Default, default_func)
    _copy_attrs(default_func, m)
    return m


def _is_a(x, y):
    '''Returns true if x == y or x is a subclass of y. Works with tuples
       by calling _is_a on their corresponding elements.

    '''
    def both(a, b, typeslist):
        return isinstance(a, typeslist) and isinstance(b, typeslist)
    if both(x, y, (tuple)):
        return all(map(_is_a, x, y))
    else:
        if both(x, y, _type_classes):
            return issubclass(x, y)
        else:
            return is_a(x, y)


@multidispatch
def is_a(x, y):
    '''Returns true if x is a y.  By default, if x == y.

    Since is_a is used internally by multimethods, and is itself a
    multimethod, infinite recursion is possible *if* the dispatch
    values cycle among two or more non-default is_a dispatches.

    '''
    return x == y


@is_a.method((object, AnythingType))
def _is_a_anything(x, y):
    '''x is always an Anything'''
    return True


__all__ = ['MultiMethod', 'type_dispatch', 'single_type_dispatch',
           'multimethod', 'Default', 'multidispatch', 'singledispatch',
           'Anything']
