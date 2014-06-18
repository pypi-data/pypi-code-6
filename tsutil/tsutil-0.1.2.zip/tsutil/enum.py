#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Turbidsoul Chen
# @Date:   2014-06-18 16:39:48
# @Last Modified by:   Turbidsoul Chen
# @Last Modified time: 2014-06-18 16:44:34

import string


class EnumMetaClass:

    def __init__(self, name, bases, dict):
        for base in bases:
            if base.__class__ is not EnumMetaClass:
                raise TypeError, "Enumeration base class must be enumeration"
        bases = filter(lambda x: x is not Enum, bases)
        self.__name__ = name
        self.__bases__ = bases
        self.__dict = {}
        for key, value in dict.items():
            self.__dict[key] = EnumInstance(name, key, value)

    def __getattr__(self, name):
        if name == '__members__':
            return self.__dict.keys()

        try:
            return self.__dict[name]
        except KeyError:
            for base in self.__bases__:
                try:
                    return getattr(base, name)
                except AttributeError:
                    continue

        raise AttributeError, name

    def __repr__(self):
        s = self.__name__
        if self.__bases__:
            s = s + '(' + string.join(map(lambda x: x.__name__,
                                          self.__bases__), ", ") + ')'
        if self.__dict:
            list = []
            for key, value in self.__dict.items():
                list.append("%s: %s" % (key, int(value)))
            s = "%s: {%s}" % (s, string.join(list, ", "))
        return s

    def names(self):
        return [name for name in self.__dict.keys() if not name.startswith('__')]

    def values(self):
        return [item[1].value for item in self.__dict.items() if not item[0].startswith('__')]

    def value_of(self, name):
        return self.__getattr__(name)


class EnumInstance:

    def __init__(self, classname, enumname, value):
        self.__classname = classname
        self.__enumname = enumname
        self.__value = value

    def __int__(self):
        return self.__value

    def __repr__(self):
        return "EnumInstance(%s, %s, %s)" % (`self.__classname`,
                                             `self.__enumname`,
                                             `self.__value`)

    def __str__(self):
        return "%s.%s" % (self.__classname, self.__enumname)

    def __cmp__(self, other):
        if not isinstance(other, EnumInstance):
            return True
        return cmp(self.name, other.name)

    @property
    def value(self):
        return self.__value

    @property
    def name(self):
        return self.__enumname


Enum = EnumMetaClass("Enum", (), {})