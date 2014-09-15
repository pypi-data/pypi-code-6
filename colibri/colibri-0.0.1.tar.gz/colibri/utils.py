# -*- coding: utf-8 -*-
"""
colibri.utils
~~~~~~~~~~~~~

Various useful classes and functions.

"""
from __future__ import absolute_import

from asyncio import async
from collections import Iterable, Mapping


class cached_property(object):
    """Property descriptor that caches the return value
    of the get function.

    *Examples*

    .. code-block:: python

        @cached_property
        def connection(self):
            return Connection()
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        r = instance.__dict__[self.func.__name__] = self.func(instance)
        return r


def is_list(obj, scalars=(Mapping, str), iterables=(Iterable, )):
    """Return True if the object is iterable, but not if object is one
    of `scalars`."""
    return isinstance(obj, iterables) and not isinstance(obj, scalars or ())


def maybe_list(obj, scalars=(Mapping, str)):
    """Return list of one element if `obj` is a scalar."""
    return obj if obj is None or is_list(obj, scalars) else [obj]


def chunks(iterable, chunk_size):
    """Yield successive `chunk_size`d chunks from `iterable`."""
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i+chunk_size]


class YieldFromContextManager(object):
    """Context manager.

    This enables the following idiom for opening and closing an
    object around a block:

        with (yield from obj):
            <block>

    while failing loudly when accidentally using:

        with obj:
            <block>
    """

    def __init__(self, obj):
        self._obj = obj

    def __enter__(self):
        return self._obj

    def __exit__(self, *args):
        try:
            # contextmanager does not yield from __exit__
            async(self._obj.close())
        finally:
            self._obj = None  # Crudely prevent reuse
