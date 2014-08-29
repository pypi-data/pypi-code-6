__all__ = ['NList']
__doc__ = """This module provides class :class:`NList`, a multidimensional list.

Indexes and shapes used with NList must be tuples.
Example:
::

    l = nlist.NList(shape=(2, 3))
    l[1, 2] = 42

NList's shape can be an empty tuple meaning a zero-dimensional list that has
one element with index ().

NList converts to False only if its :attr:`size` is 0, meaning that
at least one of its dimensions is 0. Note that the :attr:`size` of a
zero-dimensional NList is 1.

An NList equals another NList if their shapes and all their elements are equal.

NList is an iterable of all its elements.

Whenever an ordering of indexes is implied,
standard tuple comparison semantics are used.
"""

import operator
import itertools
from itertools import islice
from collections.abc import Container, Iterable, Sequence
from functools import reduce


def product(l):
    return reduce(operator.mul, l, 1)

def group_every_n(l, n):
    rest = l
    while True:
        rest1, rest2 = itertools.tee(rest)
        group, rest = list(islice(rest1, n)), islice(rest2, n, None)
        if not group:
            break
        yield group


class NList:
    """Initialize NList either from another multidimensional structure
    or by shape and default value.

    :param other: Either an another NList or a nested sequence to copy data from.
        For instance, if other is [[1, 2, 3], [4, 5, 6]], a 2x3 NList will be
        created with this data.
    :param tuple shape: A tuple of dimension sizes. E.g. (2, 3) for 2x3 NList.
    :param default: A value to fill the NList with when `shape` is passed.

    `other` and `shape`/`default` arguments are mutually exclusive
    """
    def __init__(self, other=None, shape=None, default=None):
        if other is not None:
            if shape is not None or default is not None:
                raise RuntimeError(
                    "'other' and 'shape'/'default' arguments are mutually exclusive"
                )

            if isinstance(other, NList):
                self._init_from_nlist(other)
            elif isinstance(other, Sequence):
                self._init_from_nested(other)
            else:
                raise TypeError("'other' must be either NList or a Sequence")
        else:
            if shape is None:
                shape = ()
            self._init_from_shape(shape, default)

    def _init_from_nlist(self, other):
        self._data = other._data.copy()
        self._shape = other.shape
        self._strides = other._strides

    def _init_from_nested(self, other):
        shape = [len(other)]
        values = other
        while True:
            if (all(isinstance(x, Sequence) for x in values) and
                    len({len(x) for x in values}) == 1):
                shape.append(len(values[0]))
                values = list(itertools.chain(*values))
            else:
                break
        self._shape = tuple(shape)
        self._build_strides()
        self._data = values

    def _init_from_shape(self, shape, default):
        self._check_shape(shape)

        self._shape = shape
        self._build_strides()
        self._data = [default] * self.size

    def _build_strides(self):
        self._strides = tuple(
            product(self.shape[j] for j in range(k + 1, self.rank))
            for k in range(self.rank)
        )

    @property
    def shape(self):
        """A tuple with the NList's dimensions. Read-only."""
        return self._shape

    @property
    def rank(self):
        """Number of the NList's dimensions. Read-only."""
        return len(self.shape)

    @property
    def size(self):
        """Number of elements in the NList. Read-only."""
        return product(self.shape)

    def __bool__(self):
        return self.size != 0

    def __eq__(self, other):
        return (
            isinstance(other, NList) and
            self.shape == other.shape and
            self._data == other._data
        )

    def __getitem__(self, key):
        return self._data[self._index_to_flat(key)]

    def __setitem__(self, key, value):
        self._data[self._index_to_flat(key)] = value

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        nested = self._to_nested()
        return 'NList(%s, shape=%s)' % (nested, self.shape)

    def __str__(self):
        return repr(self)

    def copy(self):
        """Returns a shallow copy of the NList.

        :rtype: NList
        """
        return type(self)(other=self)

    def count(self, value):
        """Returns the number of occurrences of `value` in the NList.

        :rtype: int
        """
        return self._data.count(value)

    def keys(self, start=None, stop=None):
        """Returns an iterable of all indexes valid for the NList.

        :param tuple start: An index to start iteration from.
        :param tuple stop: An index before which to stop iteration.

        `start` and `stop` must be valid indexes for the NList, or `None`.
        """
        if start is not None:
            self._check_index(start)
        else:
            start = (0,) * self.rank
        if stop is not None:
            self._check_index(stop)

        current = start
        while self._index_in_range(current, stop):
            yield current
            current = self._next_index(current)

    def _index_in_range(self, index, stop):
        return (
            index is not None and
            self._in_bounds(index) and
            (stop is None or index < stop)
        )

    def _next_index(self, index):
        current = list(index)
        i = self.rank - 1
        while i >= 0:
            current[i] += 1

            if current[i] >= self.shape[i]:
                current[i] = 0
                i -= 1
            else:
                return tuple(current)
        else:
            return None

    def enumerate(self):
        """Return an iterable of all pairs (index, value) in the NList."""
        for key in self.keys():
            yield (key, self[key])

    def index(self, value, start=None, stop=None):
        """Returns index of the first occurrence of `value` in the NList.

        :param value: A value to search for.
        :param tuple start: An index to start the search from.
        :param tuple stop: An index before which to stop search.
        :raises ValueError: If the value is not found.
        :rtype: tuple

        `start` and `stop` must be valid indexes for the NList, or `None`.
        """
        for key in self.keys(start, stop):
            if self[key] == value:
                return key
        raise ValueError('%s is not in the NList' % value)

    def _to_nested(self):
        if self.rank == 0:
            return self._data[0]
        if self.size == 0:
            return []

        nested = self._data
        for dim in reversed(self.shape[1:]):
            nested = group_every_n(nested, dim)
        return list(nested)

    def _check_index(self, index):
        if not isinstance(index, tuple):
            raise TypeError('NList index must be a tuple')
        if len(index) != self.rank:
            raise TypeError('NList index must be rank %s' % self.rank)
        if any(not isinstance(x, int) for x in index):
            raise TypeError('Indexes must consist of integers')
        if not self._in_bounds(index):
            raise IndexError('NList index out of range')

    def _in_bounds(self, index):
        for i, x in enumerate(index):
            if not 0 <= x < self.shape[i]:
                return False
        return True

    def _index_to_flat(self, index):
        self._check_index(index)
        return sum(self._strides[k] * index[k] for k in range(self.rank))

    @staticmethod
    def _check_shape(shape):
        for x in shape:
            if not isinstance(x, int):
                raise TypeError('Dimensions must be integers')
            if x < 0:
                raise ValueError('Dimensions cannot be negative')

Container.register(NList)
Iterable.register(NList)
