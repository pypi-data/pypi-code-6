# -*- coding: UTF-8 -*-
'''\

The contents of the module :mod:`pytrapal.selectors` serve as item selectors
for PyTraPaL paths. The functions in this module break the convention
of using lower case for their names to prevent name clashes with functions and
classes in the Python standard library as well as making path definitions
easier to be read.

The item selectors are categorized by what they work on:

*   :ref:`attributes`
*   :ref:`iterables`

    *   :ref:`sequences`
    *   :ref:`mappings`
    *   :ref:`sets`

*   :ref:`others`


.. _attributes:

Attributes of Input Items
^^^^^^^^^^^^^^^^^^^^^^^^^

The following objects work on the attributes of input items.

.. autofunction:: Dir

.. autofunction:: AttrValues

.. autofunction:: Attrs

.. autoclass:: GetAttr

.. attribute:: Attr

    An object which on retrieving an arbitrary attribute's (except for
    ``__getattr__`` and all attributes of :class:`object`) value returns an
    instance of :class:`GetAttr` initialized with the name of the attribute.

    Example:

    ..
        >>> class Foo(object):
        ...     foo = 0

        >>> class Bar(object):
        ...     bar = 1

        >>> class FooBar(object):
        ...     foo = 2
        ...     bar = 3

    >>> list(Attr.foo([Foo, Bar, FooBar], None))
    [0, 2]


.. _iterables:

Iterable Input Items
^^^^^^^^^^^^^^^^^^^^
The following objects work on iterable input items.

.. autofunction:: Iter

.. autoclass:: GetItem

.. attribute:: Item

    An object which on retrieving an item or attribute returns an instance of
    :class:`GetItem` initialized with the attribute name or key/index of the
    item.

    Example:

    >>> list(Item.foo([{'foo': 0}, {'bar': 1}, {'foo': 2}], None))
    [0, 2]
    >>> list(Item[0]([(0, 1), [], (1, 2, 3)], None))
    [0, 1]


.. _sequences:

Sequences
"""""""""
.. autofunction:: Enumerate

.. autoclass:: GetSlice

.. attribute:: Slice

    An object which on retrieving a slice returns an instance of
    :class:`GetSlice` initialized with the slice.

    Example:

    >>> list(Slice[1:3]([(-1, 0, 1, -2), [], (1, 2)], None))
    [0, 1, 2]


.. _mappings:

Mappings
""""""""
.. autofunction:: Items

.. autofunction:: Values


.. _sets:

Set-Operations
""""""""""""""
.. autofunction:: Set

.. autofunction:: Union

.. autofunction:: Intersection

.. autofunction:: Difference

.. autofunction:: SymmetricDifference


.. _others:

Other Types
^^^^^^^^^^^
The following objects work on other or arbitrary types.

.. autoclass:: Call

.. autoclass:: DepthWalk

.. autoclass:: BreadthWalk

.. autoclass:: Sorted

.. autoclass:: Filter

.. autofunction:: Identity

.. autoclass:: Map

.. autoclass:: Reduce(func[, initializer])

.. autoclass:: Sum

'''

import sys
if sys.version_info.major > 2:
    _filter = filter
    _map = map
else:
    import itertools
    _filter = itertools.ifilter
    _map = itertools.imap
    del itertools
del sys


class Sorted(object):
    '''\
    Instances are item selectors returning a :class:`list` of the input items.

    ``key`` receives one argument (the item) and is used like the ``key``
    argument of :func:`sorted`, the latter is being used for sorting.

    :param key: The sorting key callable or :const:`None` if default sorting
        should be used.
    :param reverse: If reverse sorting should be used.

    Examples:

    >>> Sorted()(['b', 'a', 'c'])
    ['a', 'b', 'c']
    >>> Sorted(lambda item: -item, True)([2, 1, 4, 3])
    [1, 2, 3, 4]
    '''
    def __init__(self, key=None, reverse=False):
        self._key = key
        self._reverse = reverse

    def __call__(self, items, **kargs):
        if self._key is None:
            func = None
        else:
            func = lambda item: self._key(item)
        return sorted(items, key=func, reverse=self._reverse)


class Filter(object):
    '''\
    Instances are item selectors returning an iterator over only those input
    items, for which the callable ``predicate`` returns :const:`True`. If the
    predicate is :const:`None`, the items are returned which are
    :const:`True`.

    ``predicate`` receives one argument (the item) and is used like the
    ``predicate`` argument of :func:`itertools.ifilter` (Python
    2)/:func:`filter` (Python 3), the latter are being used for sorting.

    :param predicate: The callable used for filtering or :const:`None` to
        return items which are :const:`True`.

    Examples:

    >>> list(Filter(lambda item: 0 < item < 4)([1, 2, 3, 4, 5]))
    [1, 2, 3]
    >>> list(Filter(None)([0, [], [1, 2], 1, True, False]))
    [[1, 2], 1, True]
    '''
    def __init__(self, predicate):
        self._predicate = predicate

    def __call__(self, items, **kargs):
        if self._predicate is None:
            func = None
        else:
            func = lambda item: self._predicate(item)
        return _filter(func, items)


class Map(object):
    '''\
    Instances are an item selector returning an iterator over the results of
    calling ``func`` each the item.

    ``func`` receives one argument (the item) and is used like the ``func``
    argument of :func:`itertools.imap` (Python 2)/:func:`map` (Python 3), the
    latter are being used for sorting.

    :param func: The callable used on each item.


    Example:

    >>> list(Map(lambda item: item + 1)([0, 1, 2]))
    [1, 2, 3]
    '''
    def __init__(self, func):
        self._func = func

    def __call__(self, items, **kargs):
        func = lambda item: self._func(item)
        return _map(func, items)


def Dir(items, error_handler, **kargs):
    '''\
    This item selector (a generator) returns an iterator over the attribute
    names of the input items. The same name may occur multiple times. All
    :class:`AttributeError` instances are silently dropped, ``error_handler``
    is called with the other exceptions.

    Example:

    >>> class Test(object):
    ...     foo = 1
    ...     bar = 2

    >>> sorted(filter(lambda name: not name.startswith('_'), Dir([Test], lambda e: None)))
    ['bar', 'foo']
    '''
    for item in items:
        for name in dir(item):
            try:
                yield name
            except AttributeError:
                pass
            except Exception as e:
                error_handler(e)


def Attrs(items, error_handler, **kargs):
    '''\
    This item selector (a generator) returns an iterator over 2-:class:`tuple`
    objects, containing the name and the value of the attributes of the input
    items. The same name-value combination may occur multiple times. All
    :class:`AttributeError` instances are silently dropped, ``error_handler``
    is called with the other exceptions.

    Example:

    ..
        >>> class Test(object):
        ...     foo = 1
        ...     bar = 2

    >>> sorted(filter(lambda attr: not attr[0].startswith('_'), Attrs([Test], lambda e: None)))
    [('bar', 2), ('foo', 1)]
    '''
    for item in items:
        for name in dir(item):
            try:
                yield (name, getattr(item, name))
            except AttributeError:
                pass
            except Exception as e:
                error_handler(e)


def AttrValues(items, error_handler, **kargs):
    '''\
    This item selector (a generator) returns an iterator over the attribute
    values of the input items. The same value may occur multiple times. All
    :class:`AttributeError` instances are silently dropped, ``error_handler``
    is called with the other exceptions.

    Example:

    ..
        >>> class Test(object):
        ...     foo = 1
        ...     bar = 2

    >>> sorted(filter(lambda value: isinstance(value, int), AttrValues([Test], lambda e: None)))
    [1, 2]
    '''
    for item in items:
        for name in dir(item):
            try:
                yield getattr(item, name)
            except AttributeError:
                pass
            except Exception as e:
                error_handler(e)


class GetAttr(object):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over the value of the attribute with the specified
    name for each input item, which does not raise an :class:`AttributeError`
    on retrieving the value (those exceptions are silently dropped).
    ``error_handler`` is called with the other exceptions.

    :param name: The name of the attribute to retrieve.

    Example:

    ..
        >>> class Foo(object):
        ...     foo = 0

        >>> class Bar(object):
        ...     bar = 1

        >>> class FooBar(object):
        ...     foo = 2
        ...     bar = 3

    >>> foo_values = GetAttr('foo')
    >>> list(foo_values([Foo, Bar, FooBar], None))
    [0, 2]
    '''
    def __init__(self, name):
        self._name = name

    def __call__(self, items, error_handler, **kargs):
        for item in items:
            try:
                yield getattr(item, self._name)
            except AttributeError:
                pass
            except Exception as e:
                error_handler(e)


class Attr(object):
    def __getattr__(self, name):
        return GetAttr(name)

Attr = Attr()



def Iter(items, error_handler, **kargs):
    '''\
    This item selector (a generator) returns an iterator over the items of all
    iterable input items. All :class:`TypeError` instances are silently
    dropped, ``error_handler`` is called with the other exceptions.

    Example:

    >>> list(Iter([(1, 2, 3), -1, (4, 5, 6), False], None))
    [1, 2, 3, 4, 5, 6]
    '''
    for item in items:
        try:
            for value in item:
                yield value
        except TypeError:
            pass
        except Exception as e:
            error_handler(e)


def Enumerate(items, error_handler, **kargs):
    '''\
    This item selector (a generator) returns an iterator over the items of the
    call of :func:`enumerate` on each item, for which no :class:`TypeError` is
    thrown – those exceptions are silently dropped. ``error_handler`` is
    called with the other exceptions.

    Example:

    >>> list(Enumerate([(1, 2, 3), -1, (4, 5, 6), False], None))
    [(0, 1), (1, 2), (2, 3), (0, 4), (1, 5), (2, 6)]
    '''
    for item in items:
        try:
            for value in enumerate(item):
                yield value
        except TypeError:
            pass
        except Exception as e:
            error_handler(e)


def Items(items, error_handler, **kargs):
    '''\
    This item selector (a generator) returns an iterator over 2-:func:`tuple`
    instances containing the key and value for each entry of all mapping-type
    input items. All :class:`TypeError` instances are silently dropped,
    ``error_handler`` is called with the other exceptions.

    Example:

    >>> sorted(Items([{'foo': 1, 'bar': 0}, -1, {'foo': 2, 'foobar': 3}, False], None))
    [('bar', 0), ('foo', 1), ('foo', 2), ('foobar', 3)]
    '''
    for item in items:
        try:
            for key in item:
                yield key, item[key]
        except TypeError:
            pass
        except Exception as e:
            error_handler(e)


def Values(items, error_handler, **kargs):
    '''\
    This item selector (a generator) returns an iterator over the values of
    the entries of all mapping-type input items. All :class:`TypeError`
    instances are silently dropped, ``error_handler`` is called with the other
    exceptions.

    Example:

    >>> sorted(Values([{'foo': 1, 'bar': 0}, -1, {'foo': 2, 'foobar': 3}, False], None))
    [0, 1, 2, 3]
    '''
    for item in items:
        try:
            for key in item:
                yield item[key]
        except TypeError:
            pass
        except Exception as e:
            error_handler(e)


class GetItem(object):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over the value of the item with the specified
    key/index for each input item which does not raise a :class:`KeyError`,
    :class:`IndexError` or :class:`TypeError` on retrieving the value (those
    exceptions are silently dropped). ``error_handler`` is called with the
    other exceptions.

    :param key: The key or index of the attribute to retrieve.

    Example:

    >>> foo_values = GetItem('foo')
    >>> list(foo_values([{'foo': 0}, {'bar': 1}, {'foo': 2}, None], None))
    [0, 2]
    >>> first_values = GetItem(0)
    >>> list(first_values([(0, 1), [], (1, 2, 3), None], None))
    [0, 1]
    '''
    def __init__(self, key):
        self._key = key

    def __call__(self, items, error_handler, **kargs):
        for item in items:
            try:
                yield item[self._key]
            except (KeyError, IndexError, TypeError):
                pass
            except Exception as e:
                error_handler(e)


class Item(object):
    def __getitem__(self, key):
        return GetItem(key)

    __getattr__ = __getitem__

Item = Item()


class GetSlice(object):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over the items of the slice with the specified
    key/index for each input item, which does not raise a :class:`IndexError`
    or :class:`TypeError` on retrieving the slice (those exceptions are
    silently dropped). ``error_handler`` is called with the other exceptions.

    :param slce: The slice to retrieve.
    :type slcs: :class:`slice`
    :raises ValueError: If ``slce`` is not a :class:`slice`.

    Example:

    >>> second_and_third = GetSlice(slice(1, 3))
    >>> list(second_and_third([(-1, 0, 1, -2), [], (1, 2), None], None))
    [0, 1, 2]
    >>> first_values = GetSlice(1)
    Traceback (most recent call last):
    ValueError: Only a slice may be supplied.
    '''
    def __init__(self, slce):
        if not isinstance(slce, slice):
            raise ValueError('Only a slice may be supplied.')
        self._slice = slce

    def __call__(self, items, error_handler, **kargs):
        for item in items:
            try:
                for value in item[self._slice]:
                    yield value
            except (TypeError, IndexError):
                pass
            except Exception as e:
                error_handler(e)


class Slice(object):
    def __getitem__(self, slce):
        return GetSlice(slce)

Slice = Slice()


def Identity(items, **kargs):
    '''\
    An item selector (a generator) returning an iterator over each input item.
    '''
    for item in items:
        yield item


class Call(object):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over the results of calling each input item, which
    does not raise a :class:`TypeError` or :class:`ValueError` on calling
    (those exceptions are silently dropped), with the arguments given on
    instantiation. ``error_handler`` is called with the other exceptions.

    :param args: The positional arguments for calling.
    :param kargs: The named arguments for calling.

    Example:

    >>> call = Call('0')
    >>> list(call([str, dict, bool, int], None))
    ['0', True, 0]
    '''
    def __init__(self, *args, **kargs):
        self._args = args
        self._kargs = kargs

    def __call__(self, items, error_handler, **kargs):
        for item in items:
            try:
                yield item(*self._args, **self._kargs)
            except (TypeError, ValueError):
                pass
            except Exception as e:
                error_handler(e)


class _Walk(object):
    def __init__(self, *path_steps):
        from pytrapal import Path
        self._path = Path(*path_steps)
        import collections
        self._deque = collections.deque


class DepthWalk(_Walk):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over each item given as well as the results of
    recursively calling the given path on each result in depth-first
    traversal.

    :param path_steps: The path steps for the path to apply to each item.

    Example:

    >>> items = [
    ...     {
    ...         'id': 0,
    ...         'children': [
    ...                 {'id': 1},
    ...                 {
    ...                     'id': 2,
    ...                     'children': [{'id': 3},]
    ...                 }
    ...             ]
    ...     },
    ...     {
    ...         'id': 4,
    ...         'children': [{'id': 5}, {'id': 6}],
    ...     },
    ...     {'id': 7}
    ... ]

    >>> from pytrapal import Path

    >>> depth_first_ids = Path(DepthWalk(Path(Item['children'], Iter)), Item['id'])
    >>> list(depth_first_ids(items))
    [0, 1, 2, 3, 4, 5, 6, 7]
    '''
    def __call__(self, items, env, error_handler):
        current_results = []
        pending_results = self._deque(items)
        while len(current_results) > 0 or len(pending_results) > 0:
            if len(current_results) > 0:
                current_results.reverse()
                pending_results.extendleft(current_results)
            current_result = pending_results.popleft()
            current_results = self._path([current_result], env, error_handler)
            yield current_result


class BreadthWalk(_Walk):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over each item given as well as the results of
    recursively calling the given path on each result in breadth-first
    traversal.

    :param path_steps: The path steps for the path to apply to each item.

    Example:

    ..
        >>> items = [
        ...     {
        ...         'id': 0,
        ...         'children': [
        ...                 {'id': 1},
        ...                 {
        ...                     'id': 2,
        ...                     'children': [{'id': 3},]
        ...                 }
        ...             ]
        ...     },
        ...     {
        ...         'id': 4,
        ...         'children': [{'id': 5}, {'id': 6}],
        ...     },
        ...     {'id': 7}
        ... ]

        >>> from pytrapal import Path

    >>> breadth_first_ids = Path(BreadthWalk(Path(Item['children'], Iter)), Item['id'])
    >>> list(breadth_first_ids(items))
    [0, 4, 7, 1, 2, 5, 6, 3]
    '''
    def __call__(self, items, env, error_handler):
        pending_items = self._deque()
        pending_results = self._deque(items)
        while len(pending_items) > 0 or len(pending_results) > 0:
            if len(pending_items) > 0:
                current_results = self._path(pending_items, env,
                    error_handler)
                pending_items.clear()
                if len(current_results) > 0:
                    pending_results.extend(current_results)
            while len(pending_results) > 0:
                current_result = pending_results.popleft()
                pending_items.append(current_result)
                yield current_result


class Reduce(object):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over at most one item by reducing the input items by
    calling ``func`` consecutively on the current value and the next input
    item. If ``initializer`` is given, this serves as the first current value,
    otherwise the first item is used for that purpose. Consequently, if there
    is only one input item and no initializer given, this item is the single
    result item.

    ``func`` receives two arguments, the current value and the current item.

    The :mod:`pytrapal` API does not call item selectors with zero input
    items, but if this occurs and no initializer is given, a
    :class:`IndexError` is raised.

    Example:

    >>> sum = Reduce(lambda current, item: current + item, initializer=0)
    >>> list(sum([1, 2, 3], None))
    [6]
    >>> list(sum([], None))
    [0]
    '''
    def __init__(self, func, **kargs):
        self._func = func
        try:
            self._initializer = kargs['initializer']
        except KeyError:
            pass

    def __call__(self, items, error_handler, **kargs):
        try:
            current = self._initializer
            first_item = 0
        except AttributeError:
            current = items[0]
            first_item = 1
        if first_item is not False:
            for item in items[first_item:]:
                try:
                    current = self._func(current, item)
                except Exception as e:
                    error_handler(e)
            yield current


class Sum(object):
    '''\
    Instances are item selectors (:meth:`__call__` being a generator)
    returning an iterator over a single item being the sum of the items, using
    ``initializer`` as the starting value.

    Example:

    >>> list(Sum(-6)([1, 2, 3], None))
    [0]
    '''
    def __init__(self, initializer=0):
        self._initializer = initializer

    def __call__(self, items, error_handler, **kargs):
        current = self._initializer
        for item in items:
            try:
                current += item
            except TypeError:
                pass
            except Exception as e:
                error_handler(e)
        yield current


# Set

def Set(items, **kargs):
    '''\
    An item selector returning each (hashable) input item only
    once, leaving out those elements which are not hashable.

    Example:

    >>> non_hashable = {'foo': 'bar'}
    >>> list(Set([1, 2, 3, 1, 2, non_hashable, 3, 4, non_hashable]))
    [1, 2, 3, 4]
    '''
    data = set()
    for item in items:
        try:
            if item not in data:
                data.add(item)
                yield item
        except TypeError:
            pass


def Union(items, **kargs):
    '''\
    An item selector (a generator) returning an iterator over each element of
    the union of all iterable input items, leaving out those elements which
    are not hashable.

    Example:

    ..
        >>> non_hashable = {'foo': 'bar'}

    >>> list(Union([(1, 2, 1), (2, 3, non_hashable), -1, (4, 5)]))
    [1, 2, 3, 4, 5]
    '''
    data = set()
    for item in items:
        try:
            for value in item:
                try:
                    if value not in data:
                        data.add(value)
                        yield value
                except TypeError:
                    pass
        except TypeError:
            pass


def _sets_iterator(items):
    for item in items:
        current_set = set()
        try:
            for value in item:
                try:
                    current_set.add(value)
                except TypeError:
                    pass
        except TypeError:
            pass
        else:
            if len(current_set) > 0:
                yield current_set


def _SetItemSelector(items, set_method):
    sets = _sets_iterator(items)
    try:
        first = next(sets)
    except StopIteration:
        pass
    else:
        set_method(first, *sets)
        for result in first:
            yield result


def Intersection(items, **kargs):
    '''\
    An item selector (a generator) returning an iterator over each element of
    the intersection (using :meth:`set.intersection_update`) of all iterable
    input items, leaving out those elements which are not hashable. The first
    set for this operation is the first iterable input item containing at
    least one hashable item.

    Example:

    ..
        >>> non_hashable = {'foo': 'bar'}

    >>> list(Intersection([None, (non_hashable, ), (1, 2, 3, 4), (2, 3, 5), (3, non_hashable, 4, 2)]))
    [2, 3]
    '''
    return _SetItemSelector(items, set.intersection_update)


def Difference(items, **kargs):
    '''\
    An item selector (a generator) returning an iterator over each element of
    the set difference (using :meth:`set.difference_update`) of all iterable input
    items leaving out those elements which are not hashable. The first set for
    this operation is the first iterable input item containing at least one
    hashable item.

    Example:

    ..
        >>> non_hashable = {'foo': 'bar'}

    >>> list(Difference([None, (non_hashable,), (0, 1, 2, 3, 4, 5), (2, 3), (4, non_hashable, 5)]))
    [0, 1]
    '''
    return _SetItemSelector(items, set.difference_update)


def SymmetricDifference(items, **kargs):
    '''\
    An item selector (a generator) returning an iterator over each element of
    the symmetric set difference (using
    :meth:`set.symmetric_difference_update` multiple times) of all iterable
    input items leaving out those elements which are not hashable. The first
    set for this operation is the first iterable input item containing at
    least one hashable item.

    Example:

    ..
        >>> non_hashable = {'foo': 'bar'}

    >>> list(SymmetricDifference([None, (non_hashable,), (-1, 0, 2, 3), (-1, 1, 3, 4), (non_hashable, 4, 2)]))
    [0, 1]
    '''
    sets = _sets_iterator(items)
    try:
        first = next(sets)
    except StopIteration:
        pass
    else:
        for other in sets:
            first.symmetric_difference_update(other)
        for result in first:
            yield result
