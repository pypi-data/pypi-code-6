# -*- coding: utf-8 -*-
from __future__ import print_function


class Parameters:
    __slot__ = ('args', 'kwargs')

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        return func(*self.args, **self.kwargs)

    def __str__(self):
        items = []
        items.extend(map(repr, self.args))
        items.extend(map(lambda kv: '{}={!r}'.format(*kv), self.kwargs.items()))
        return ', '.join(items)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self)


class CallIt(Parameters):
    __slot__ = ('args', 'kwargs')


__all__ = ['Parameters', 'CallIt']
