# Copyright 2012, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""fx.itemgetter - item getter."""

__all__ = ['_', 'x']

import sys
from functools import reduce
from itertools import islice


class ItemGetter(object):
    """Proxy object provides deferred getitem logic.

    Instance of ``ItemGetter`` is meant to be used as a factory
    >>> _ = ItemGetter()

    For someone unfamiliar with lisp terminology, think ``car`` as ``head`` or
    ``first``, ``crd`` as ``tail`` or ``rest``.
    >>> car = _[0]
    >>> car([1, 2, 3])
    1
    >>> cdr = _[1:]
    >>> cdr([1, 2, 3])
    [2, 3]
    >>> cadr = _[1:][0]
    >>> cadr([1, 2, 3])
    2
    >>> cadr = cdr[0]
    >>> cadr([1, 2, 3])
    2
    >>> get_name = _['name']
    >>> get_name({'name': 'Joe', 'age': 42})
    'Joe'
    """
    def __init__(self):
        self.keys = []

    def __getitem__(self, key):
        getter = type(self)()
        getter.keys = self.keys[:]
        getter.keys.append(key)
        return getter

    def __call__(self, obj):
        def get(obj, key):
            """The item getter"""
            if hasattr(obj, '__getitem__'):
                return obj[key]

            if isinstance(key, slice):
                start, stop, step = key.start, key.stop, key.step
                return (item for item in islice(obj, start, stop, step))

            if not isinstance(key, int) or not 0 <= key <= sys.maxsize:
                raise ValueError('key must be an integer: 0 <= x <= maxsize')

            for index, item in enumerate(obj):
                if index == key:
                    return item

            raise IndexError('index out of range')

        return reduce(get, self.keys, obj)


#: ItemGetter factory object
_ = x = ItemGetter()
