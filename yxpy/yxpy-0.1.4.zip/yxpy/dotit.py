# -*- coding: utf-8 -*-
from collections import OrderedDict, Mapping


class DotDict(dict):
    __setattr__ = dict.__setitem__

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError('%r has not attr %r' % (self, name))

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError('%r has not attr %r' % (self, name))


class DotOrderedDict(OrderedDict):
    def __getattr__(self, name):
        if name.startswith('_OrderedDict'):
            raise AttributeError('%r has not attr %r' % (self, name))
        try:
            return self[name]
        except KeyError:
            raise AttributeError('%r has not attr %r' % (self, name))

    def __setattr__(self, name, value):
        if name.startswith('_OrderedDict'):
            return OrderedDict.__setattr__(self, name, value)
        self.__setitem__(name, value)

    def __delattr__(self, name):
        try:
            OrderedDict.__delitem__(self, name)
        except KeyError:
            raise AttributeError('%r has not attr %r' % (self, name))

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(('{}={!r}'.format(*i) for i in self.items())))


class DotIt(dict):
    def __init__(self, o):
        self.update(o)

    def __getattr__(self, name):
        try:
            value = self[name]
        except KeyError:
            raise AttributeError('%r has not attr %r' % (self, name))
        else:
            if isinstance(value, Mapping):
                return DotIt(value)
            return value

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError('%r has not attr %r' % self, name)
