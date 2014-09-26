# -*- coding: utf-8 -*-
from collections import OrderedDict


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
    def __init__(self, *args, **kwds):
        OrderedDict.__init__(self, *args, **kwds)

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
        OrderedDict.__delitem__(self, name)

    def __str__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(('{}={!r}'.format(*i) for i in self.items())))


class DotIt(object):
    def __init__(self, o):
        self.__dotit_o__ = o

    def __getattr__(self, name):
        try:
            return self.__dotit_o__[name]
        except KeyError:
            raise AttributeError('%r has not attr %r' % (self, name))

    def __setattr__(self, name, value):
        if name == '__dotit_o__':
            return object.__setattr__(self, name, value)
        self.__dotit_o__[name] = value

    def __delattr__(self, name):
        try:
            del self.__dotit_o__[name]
        except KeyError:
            raise AttributeError('%r has not attr %r' % self, name)
