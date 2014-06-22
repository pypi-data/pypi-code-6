#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Singleton(type):
    """
    >>> class SingleFoo(object): __metaclass__ = Singleton;
    >>> foo1 = SingleFoo()
    >>> foo1.bar = 1
    >>> foo2 = SingleFoo()
    >>> foo2.bar
    1
    >>> foo1 == foo2
    True
    """
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instance


# vim: filetype=python
