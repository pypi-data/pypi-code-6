'''\
TinkerPy
========

This Python 2 and 3 package (tested with CPython 2.7 and 3.3  as well as PyPy
2) provides:

*   funtionality related to :ref:`Python 2 versus 3 <python2vs3>`
*   special :ref:`mapping implementations <mappings>`
*   some useful :ref:`decorators <decorators>`
*   :ref:`SAX handlers <sax_handlers>`
*   :ref:`other <others>` functionality like a class handling integers
    represented as strings (:class:`StrIntegers`) special list implementation
    (:class:`AllowingList`), the :func:`flatten` function to flatten data
    structures composed of iterables and a function to create anonymous classes
    (:func:`anonymous_class`)
*   a :ref:`Finite State Machine <fsm>` implementation


.. _python2vs3:

Python 2 vs. 3
--------------

.. py:data:: PY_VERSION_GT_2

    :const:`True` for a Python runtime with the major version being greater
    than two, :const:`True` otherwise.

.. autofunction:: py2or3

.. autofunction:: metaclass

.. function:: Unicode

    For Python 2 this is :func:`unicode`, for Python 3 this is :func:`str`.

.. py:data:: STRING_TYPES

    For Python 2 this is the :func:`tuple` ``(str, unicode)``, in Python 3
    this is simply :func:`str`.


.. _mappings:

Mappings
--------

.. autoclass:: AttributeDict
.. autoclass:: ImmutableDict
.. autoclass:: ProxyDict


.. _decorators:

Decorators
----------

.. autofunction:: multi_decorator
.. autofunction:: namespace
.. autofunction:: update_globals
.. autofunction:: attribute_dict


.. _sax_handlers:

SAX Handlers
------------

.. autoclass:: LexicalHandler
.. autoclass:: DeclarationHandler


.. _others:

Others
------
.. autoclass:: StrIntegers
.. autoclass:: AllowingList
.. autofunction:: anonymous_class
.. autofunction:: flatten

'''

import collections
import abc


# Python 2 vs. 3

import sys
PY_VERSION_GT_2 = sys.version_info[0] > 2
del sys

def py2or3(py2, py3):
    '''\
    Returns one of the given arguments depending on the Python version.

    :param py2: The value to return in Python 2.
    :param py3: The value to return in Python 3.
    :returns: ``py2`` or ``py3`` depending on the Python version.
    '''
    if PY_VERSION_GT_2:
        return py3
    else:
        return py2

Unicode = py2or3(lambda: unicode, lambda: str)()
STRING_TYPES = py2or3(lambda: (str, unicode), lambda: str)()


def metaclass(metacls):
    '''\
    Creates a class decorator using the given metaclass to create a new class
    from the one which it is decorating. This allows for easier porting
    between Python 2 and 3 if using metaclasses, as it has the same effect as
    specifying a metaclass, but is usable for Python 2, 3 and higher.

    :param metacls: The metaclass to use.
    :returns: A class decorator which, when applied, calls the metaclass with
        the name, the bases and the dictionary of the decorated class.

    Example:

    First we define a metaclass which adds an attribute ``number`` to its
    class with an ever-increasing integer:

    >>> class Numbering(object):
    ...     def __init__(self):
    ...         self.number = 1
    ...
    ...     def __call__(self, name, bases, dict):
    ...         dict['number'] = self.number
    ...         self.number += 1
    ...         cls = type(name, bases, dict)
    ...         return cls
    >>> Numbering = Numbering()

    Here are two classes using the metaclass:

    >>> @metaclass(Numbering)
    ... class Foo(object):
    ...     pass

    >>> @metaclass(Numbering)
    ... class Bar(object):
    ...     pass

    >>> print(Foo.number)
    1
    >>> print(Bar.number)
    2

    '''
    def decorator(cls):
        new_cls = metacls(cls.__name__, cls.__bases__, dict(cls.__dict__))
        new_cls.__module__ = cls.__module__
        return new_cls
    return decorator


# MAPPINGS

class AttributeDict(dict):
    '''\
    A mapping like :class:`dict`, which exposes its values as attributes.

    It uses the ``__getattr__``, ``__delattr__`` and ``__setattr__`` hooks, so
    be aware of that when overriding these methods.

    If an attribute is retrieved which does not exist but who's name is a key
    in the dictionary, the dictionary value is returned.

    If an attribute is set/deleted who's name is a key in the dictionary, the
    dictionary entry is updated/deleted. Otherwise the attribute is
    created/deleted. Thus attribute values shadow attributes on
    setting/deleting attributes.

    Examples:

    >>> ad = AttributeDict((('foo', 1), ('bar', 2)))
    >>> print(ad.foo); print(ad.bar)
    1
    2
    >>> ad.foo = 3; print(ad.foo == ad['foo'])
    True
    >>> del ad['bar']
    >>> print(ad.bar)
    Traceback (most recent call last):
    AttributeError: 'bar'
    >>> print('bar' in ad)
    False
    >>> ad.bar = 2
    >>> print('bar' in ad)
    False
    '''
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        if name in self:
            self[name] = value
        else:
            dict.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            dict.__delattr__(self, name)


class ImmutableDict(collections.Mapping):
    '''\
    An immutable mapping that accepts the same constructor arguments as
    :class:`dict`.

    >>> immutable = ImmutableDict({'foo': 1, 'bar': 2})
    >>> print(immutable['foo'])
    1
    >>> del immutable['foo']
    Traceback (most recent call last):
    TypeError: 'ImmutableDict' object does not support item deletion
    >>> immutable['foo'] = 3
    Traceback (most recent call last):
    TypeError: 'ImmutableDict' object does not support item assignment
    '''
    __slots__ = {'_dict'}

    def __init__(self, *args, **kargs):
        self._dict = dict(*args, **kargs)

    def __getitem__(self, name):
        return self._dict[name]

    def __contains__(self, name):
        return name in self._dict

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return self._dict.__iter__()


class ProxyDict(collections.MutableMapping):
    '''\
    A mutable mapping serving as a proxy for another mapping. Setting values
    on the instance sets the value on the instance itself, not on the
    original, only those values can be deleted.

    Example:

    >>> original = {'foo': 0, 'bar': 1}
    >>> proxy = ProxyDict(original)
    >>> 'foo' in proxy and 'bar' in proxy
    True
    >>> proxy['foo'] = -1
    >>> original['foo'] == 0 and proxy['foo'] == -1 and len(proxy) == 2
    True
    >>> proxy['foobar'] = 2
    >>> 'foobar' in proxy and len(proxy) == 3
    True
    >>> sorted(proxy.keys())
    ['bar', 'foo', 'foobar']
    >>> del proxy['foo']
    >>> 'foo' in proxy
    True
    >>> del proxy['foo']
    Traceback (most recent call last):
    KeyError: 'foo'
    '''
    def __init__(self, original):
        self._original = original
        self._mapping = dict()

    def __getitem__(self, key):
        try:
            return self._mapping[key]
        except KeyError:
            return self._original[key]

    def __contains__(self, key):
        return key in self._mapping or key in self._original

    def __iter__(self):
        for key in self._mapping:
            yield key
        for key in self._original:
            if key not in self._mapping:
                yield key

    def __len__(self):
        length = 0
        for key in self:
            length += 1
        return length

    def __setitem__(self, key, value):
        self._mapping[key] = value

    def __delitem__(self, key):
        del self._mapping[key]

    def is_virtual(self, key):
        '''\
        Return :const:`True` if key is not set on the instance itself, but in
        the source mapping.
        '''
        return key not in self._mapping and key in self._original

    @property
    def len(self):
        '''\
        The number of items defined on the instance itself.
        '''
        return len(self._mapping)


# OTHERS

def anonymous_class(_extends=object, **attributes):
    '''\
    Creates a new-style class object extending the class ``extends`` and
    the attributes given by ``attributes``.

    :param _extends: The class to extend.
    :param attributes: The attributes of the new class.
    :returns: a new class object.

    Example:

    >>> Test = anonymous_class(
    ...     foo=lambda self: self.bar,
    ...     bar=0,
    ...     baz=classmethod(lambda cls: cls.bar),
    ...     foobar=staticmethod(lambda: 1)
    ... )

    >>> test = Test()
    >>> test.foo()
    0
    >>> Test.baz()
    0
    >>> Test.foobar()
    1
    '''
    new_name = '<anonymous:{}.{}>'.format(_extends.__module__,
        _extends.__name__)
    return type(new_name, (_extends,), attributes)


class AllowingList(collections.MutableSequence):
    '''\
    A list which checks on adding items, if the given item is allowed. This
    class should be inherited from and extending classes should specify a
    class or instance atttibute ``ALLOWED_ITEMS`` containing an iterable. Each
    item of the iterable can either be a :class:`type` object (i.e. a class),
    a callable taking one argument or a string. On adding the item is checked
    against the contents of ``ALLOWED_ITEMS``: if the item is an instance of a
    class contained there, a callable contained there returns :const:`True`
    for the item or the name of the item's class and its super-classes is
    contained there, then the item is added to the list, otherwise a
    :class:`ValueError` is thrown.

    Example:

    >>> class TestList(AllowingList):
    ...     ALLOWED_ITEMS = {'TestList', dict, lambda item: bool(item)}
    ...
    >>> t = TestList([True, ''])
    Traceback (most recent call last):
    ValueError: Invalid item: ''
    >>> t = TestList([TestList()])
    >>> t[0] = False
    Traceback (most recent call last):
    ValueError: Invalid item: False
    >>> t.append({1: 2})
    >>> t.append(0)
    Traceback (most recent call last):
    ValueError: Invalid item: 0
    >>> t.insert(0, True)
    >>> t.insert(0, False)
    Traceback (most recent call last):
    ValueError: Invalid item: False
    >>> t.extend([1, False, 'Test'])
    Traceback (most recent call last):
    ValueError: Invalid item: False
    >>> print(t)
    tinkerpy.TestList([True, tinkerpy.TestList([]), {1: 2}, 1])
    '''
    def __init__(self, iterable=None):
        if iterable is None:
            self._list = list()
        else:
            try:
                for item in iterable:
                    self._check_child_allowed(item)
            except TypeError:
                pass
            self._list = list(iterable)

    def is_allowed_child(self, item):
        '''\
        Return :const:`True` if ``item`` is an allowed item.

        :param item: The item to check.
        :returns: :const:`True` if ``item`` is a valid item.
        '''
        try:
            allowed = self.ALLOWED_ITEMS
        except AttributeError:
            return True
        def is_allowed(allowed_spec):
            if allowed_spec.__class__ is type:
                return isinstance(item, allowed_spec)
            try:
                return allowed_spec(item)
            except TypeError:
                cls_name = str(allowed_spec)
                for cls in item.__class__.__mro__:
                    if cls.__name__ == cls_name:
                        return True
                return False
        for allowed_spec in allowed:
            if is_allowed(allowed_spec):
                return True
        return False

    def _check_child_allowed(self, item):
        if not self.is_allowed_child(item):
            raise ValueError('Invalid item: {}'.format(repr(item)))

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, item):
        self._check_child_allowed(item)
        self._list[index] = item

    def __delitem__(self, index):
        del self._list[index]

    def insert(self, index, item):
        '''\
        Insert ``item`` at ``index``.
        '''
        self._check_child_allowed(item)
        self._list.insert(index, item)

    def __len__(self):
        return len(self._list)

    def __str__(self):
        object_repr = object.__repr__(self)
        object_repr = object_repr[1:object_repr.rfind(' object at ')]
        return '{}({})'.format(object_repr, self._list)

    __repr__ = __str__


def flatten(obj, *flattening_configurations):
    '''\
    Flattens iterable data structures.

    :param obj: The object to flatten. It should be an iterable.

    :param flattening_configurations: An arbitrary number of *flattening
        configurations*. A flattening configuration is a 1- or 2-tuple
        containing callables with one argument. The first callable is a test,
        which should return :const:`True` if the configuration applies to the
        given object and :const:`False` otherwise. The second callable, if
        given, is used to flatten the given object. If it does not exist, it
        is assumed to be :const:`None`.

        If no flattening configuration is given, the following is used::

            (
                (lambda obj: isinstance(obj, collections.Mapping),
                    lambda obj: obj.values()),
                (lambda obj: (isinstance(obj, collections.Iterable)
                        and not isinstance(obj, STRING_TYPES)), )
            )

    :returns: A generator returning all descendants of all of elements of
        ``obj``.


    Flattening works as follows:

    1. For each element ``e`` in the object to flatten do:

        1. Iterate over the flattening configurations:

            * If the test (the first callable of the current configuration)
              returns :const:`True`, stop iterating over the configurations
              and memorize ``e`` is flattable. If the second callable exists
              and is not :const:`None`, assign ``e`` as the result of calling
              this callable with ``e``. Otherwise ``e`` is not modified and
              memorized as being not flattable.

            * Otherwise go to next configuration.

        2. If ``e`` is flattable, flatten it and yield each resulting element.
           Otherwise yield ``e``.


    This function flattens ``obj`` as just described, creating a generator
    returning each element of each flattable descendant of ``obj``.


    Examples:

    >>> mapping = {1: 'foo', 2: 'bar'}
    >>> iterable = ('Hello', 'World', mapping)
    >>> for e in flatten(iterable):
    ...     print(e)
    Hello
    World
    foo
    bar
    >>> flattening_configs = (
    ...     (lambda obj: isinstance(obj, collections.Mapping),
    ...         lambda obj: obj.keys(), ),
    ...     (lambda obj: (isinstance(obj, collections.Iterable)
    ...             and not isinstance(obj, STRING_TYPES)), ),
    ... )
    >>> tuple(flatten(iterable, *flattening_configs))
    ('Hello', 'World', 1, 2)
    '''
    if len(flattening_configurations) == 0:
        flattening_configurations = (
            (lambda obj: isinstance(obj, collections.Mapping),
                lambda obj: obj.values(), ),
            (lambda obj: (isinstance(obj, collections.Iterable)
                    and not isinstance(obj, STRING_TYPES)), )
        )
    def _flatten(*objects):
        for obj in objects:
            flattable = False
            for flattening_configuration in flattening_configurations:
                try:
                    test, conversion  = flattening_configuration
                except ValueError:
                    test = flattening_configuration[0]
                    conversion = None
                if test(obj):
                    if conversion is not None:
                        obj = conversion(obj)
                    flattable = True
                    break
            if flattable:
                for value in _flatten(*obj):
                    yield value
            else:
                yield obj
    return _flatten(obj)


class StrIntegers(object):
    '''\
    Instances of this class care handling of integers represented as a string in
    a given base, using a lookup table. The default lookup table implements an
    alpha-numerical mapping similar to :func:`int`: first the digits 0 through
    9, then the lower-case alphabet a-z, followed by the upper-case alphabet
    A-Z. Thus the maximum base with this lookup table is 62. To consistently
    deal with lower-case letters, use the ``ignore_case`` initialization
    argument, but be sure to use an appropriate lookup table (if
    using the default this is cared for automatically).

    :param base: The base to use for conversion, this must be greater than or
        equal 2 and less than or equal the size of the lookup table. If no
        special lookup table is given, the maximum is 62.
    :type base: class:`int`
    :param ignore_case: If this is :const:`True`, all string values given are
        converted to lower case. If the default lookup table is used, it is
        trunctated to end at the lower case z.
    :type ignore_case: :class:`bool`
    :param lookup_table: The lookup table to use, an iterable of non-empty
        string values with minimum length 1. The index defines which number the
        string represents. If this is :const:`None`, the default lookup table
        consisting of the digits 0-9, the characters a-z and A-Z is used.
    :raises ValueError: If the base, the lookup table or its values are invalid.

    :
        >>> StrIntegers(1)
        Traceback (most recent call last):
        ValueError: Base must be >= 2 and <= 62.

        >>> StrIntegers(63)
        Traceback (most recent call last):
        ValueError: Base must be >= 2 and <= 62.

        >>> str_ints = StrIntegers(9, True, 'abcdefgh')
        Traceback (most recent call last):
        ValueError: Base must be >= 2 and <= 8.

        >>> str_ints = StrIntegers(lookup_table=['', '0'])
        Traceback (most recent call last):
        ValueError: The lookup table items must be Unicode strings with minimum length 1.

        >>> str_ints = StrIntegers(lookup_table=['a'])
        Traceback (most recent call last):
        ValueError: The lookup table must have a length of at least 2.
    '''
    __slots__ = {'_base', '_int_to_str_lookup', '_str_to_int_lookup',
        '_ignore_case', '_str_zero', '_str_one'}
    _invalid_base_error_message = 'Base must be >= 2 and <= {}.'
    _empty_string_error_message = 'Value must be a non-empty string (excluding a leading "-" or "+").'
    _empty_lookup_item_error_message = 'The lookup table items must be Unicode strings with minimum length 1.'
    _invalid_lookup_table_length_message = 'The lookup table must have a length of at least 2.'
    _default_lookup_table = u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _join = u''.join

    def __init__(self, base=10, ignore_case=False, lookup_table=None):
        base = int(base)
        ignore_case = bool(ignore_case)
        self._base = base
        self._ignore_case = ignore_case
        if lookup_table is None:
            if ignore_case:
                lookup_table = self._default_lookup_table[:36]
            else:
                lookup_table = self._default_lookup_table
        else:
            lookup_table = tuple(Unicode(item)[:1] for item in lookup_table)
            if len(lookup_table) < 2:
                raise ValueError(self._invalid_lookup_table_length_message)
            for item in lookup_table:
                if len(item) == 0:
                    raise ValueError(self._empty_lookup_item_error_message)
        if base < 2 or base > len(lookup_table):
            raise ValueError(self._invalid_base_error_message.format(
                len(lookup_table)))
        lookup_table = lookup_table[:base]
        self._str_zero = lookup_table[0]
        self._str_one = lookup_table[1]
        self._int_to_str_lookup = lookup_table
        self._str_to_int_lookup = {item: index
            for index, item in enumerate(lookup_table)}


    @property
    def base(self):
        '''\
        The base the instance uses for conversion.
        '''
        return self._base

    @property
    def lookup_table(self):
        '''\
        The lookup table the instance uses for conversion. It is a tuple of
        Unicode string values of length 1.
        '''
        return self._int_to_str_lookup

    def _pos_int_to_str(self, value):
        # RETURNS '' FOR value == 0
        def convert(value):
            while value != 0:
                remainder = value % self._base
                yield self._int_to_str_lookup[remainder]
                value = (value - remainder) // self._base
        result = self._join(convert(value))
        result = result[::-1]
        return result

    def int_to_str(self, value):
        '''\
        Converts an integer value to a string, inverse to what :func:`int` does,
        using the instance's base and lookup table.

        :param value: The value to convert, an arbitrary integer value.
        :type value: :class:`int`
        :returns: A string representing the given value.
        :rtype: :class:`str`

        Examples:

        >>> str_ints = StrIntegers(36)
        >>> print(str_ints.int_to_str(256))
        74
        >>> print(str_ints.int_to_str(-256))
        -74

        >>> str_ints = StrIntegers(8, True, 'abcdefgh')
        >>> print(str_ints.int_to_str(256))
        eaa

        :
            >>>
            >>> test_conversion = lambda si, v: int(si.int_to_str(v), si.base) == v
            >>> for base in range(2, 37):
            ...     str_ints = StrIntegers(base)
            ...     for value in range(-128, 129):
            ...         str_value = str_ints.int_to_str(value)
            ...         int_value = int(str_value, str_ints.base)
            ...         if int_value != value:
            ...             print('Test failed for value {} and base {}: {} => {}'.format(value, base, str_value, int_value))
            ...             break
        '''
        value = int(value)
        if value == 0:
            return self._str_zero
        if value < 0:
            negative = True
            value = -value
        else:
            negative = False
        result = self._pos_int_to_str(value)
        if negative:
            return u'-' + result
        return result

    def _prepare_str_value(self, value):
        value = Unicode(value)
        if self._ignore_case:
            value = value.lower()
        if value[0] == u'-':
            negative = True
            value = value[1:]
        else:
            negative = False
            if value[0] == u'+':
                value = value[1:]
        def prepare():
            non_zero_found = False
            for char in value:
                if char in self._int_to_str_lookup:
                    if non_zero_found:
                        yield char
                    else:
                        if char != self._str_zero:
                            non_zero_found = True
                            yield char
        value = self._join(prepare())
        if len(value) == 0:
            return negative, self._str_zero
        return negative, value

    def _str_to_pos_int(self, value):
        value = value[::-1]
        result = 0
        index = 0
        for char in value:
            digit = self._str_to_int_lookup[char]
            result += digit * self._base ** index
            index += 1
        return result

    def str_to_int(self, value):
        '''\
        Converts a string to an integer value, like :func:`int`, using the
        instance's base and lookup table. Characters not defined in the lookup
        table are ignored. If no known character is found ``0`` is returned.
        The first character may be ``'-'`` or ``'+'`` to indicate a positive
        or negative value. The time complexity of this method is in
        O(``len(value)``).

        :param value: The string representing an integer.
        :type value: Unicode string
        :returns: The integer represented by value.

        :param value: The string representing an integer.
        :type value: Unicode string

        :rtype: :class:`int`

        Examples:

        >>> str_ints = StrIntegers(36)
        >>> str_ints.str_to_int('VALUE 74')
        256
        >>> str_ints.str_to_int('- 7 4')
        -256

        >>> str_ints = StrIntegers(8, True, 'abcdefgh')
        >>> str_ints.str_to_int('0 E 1 A 2 A')
        256


        :
            >>> for base in range(2, 37):
            ...     str_ints = StrIntegers(base)
            ...     for value in range(-128, 129):
            ...         str_value = str_ints.int_to_str(value)
            ...         int_value = str_ints.str_to_int(str_value)
            ...         if int_value != value:
            ...             print('Test failed for value {} and base {}: {} (compared to {})'.format(value, base, str_value, int_value))
            ...             break

        '''
        negative, value = self._prepare_str_value(value)
        result = self._str_to_pos_int(value)
        if negative:
            return -result
        return result

    def _prepare_crement_str_int(self, value):
        negative, value = self._prepare_str_value(value)
        value = value[::-1]
        return negative, value

    def _increment_pos_str_int(self, value):
        def increment(value):
            overflow = True
            for char in value:
                if overflow:
                    digit = self._str_to_int_lookup[char]
                    digit += 1
                    if digit >= self._base:
                        yield self._str_zero
                    else:
                        overflow = False
                        yield self._int_to_str_lookup[digit]
                else:
                    yield char
            if overflow:
                yield self._str_one
        return self._join(increment(value))[::-1]

    def _decrement_pos_str_int(self, value):
        def decrement(value):
            max_digit = self._int_to_str_lookup[-1]
            underflow = True
            index = 0
            last_index = len(value) - 1
            for char in value:
                if underflow:
                    digit = self._str_to_int_lookup[char]
                    digit -= 1
                    if digit < 0:
                        yield max_digit
                    else:
                        underflow = False
                        if digit == 0:
                            if index == 0 or index < last_index:
                                yield self._str_zero
                        else:
                            yield self._int_to_str_lookup[digit]
                else:
                    if index < last_index or char != self._str_zero:
                        yield char
                index += 1
        result = self._join(decrement(value))
        return result[::-1]

    def increment(self, value):
        '''\
        Increments an arbitrary integer value given as a string by one, using
        the instance's base and lookup table. Characters not defined in the
        lookup table are ignored. If no known character is found ``1`` is
        returned. The first character may be ``'-'`` or ``'+'`` to indicate a
        positive or negative value. The time complexity of this method is in
        O(``len(value)``).

        :param value: The string representing an integer.
        :type value: Unicode string
        :returns: A string representing the incremented value.
        :rtype: Unicode string

        Examples:

        >>> str_ints = StrIntegers(36)
        >>> print(str_ints.increment('z'))
        10
        >>> print(str_ints.increment(' z z '))
        100
        >>> print(str_ints.increment('- 1 0 '))
        -z
        >>> print(str_ints.increment('-100'))
        -zz
        >>> print(str_ints.increment('- 1'))
        0
        >>> print(str_ints.increment('0'))
        1
        >>> print(str_ints.increment('1'))
        2
        >>> print(str_ints.increment('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'))
        10000000000000000000000000000000000000000000000000000

        >>> str_ints = StrIntegers(8, True, 'abcdefgh')
        >>> print(str_ints.increment(' H H H '))
        baaa
        '''
        negative, value = self._prepare_crement_str_int(value)
        if negative:
            result = self._decrement_pos_str_int(value)
            if result == self._str_zero:
                return result
            return u'-' + result
        return self._increment_pos_str_int(value)

    def decrement(self, value):
        '''\
        Decrements an arbitrary integer value given as a string by one, using
        the instance's base and lookup table. Characters not defined in the
        lookup table are ignored. If no known character is found ``-1`` is
        returned. The first character may be ``'-'`` or ``'+'`` to indicate a
        positive or negative value. The time complexity of this method is in
        O(``len(value)``).

        :param value: The string representing an integer.
        :type value: Unicode string
        :returns: A string representing the decremented value.
        :rtype: Unicode string

        Examples:

        >>> str_ints = StrIntegers(36)
        >>> print(str_ints.decrement('10'))
        z
        >>> print(str_ints.decrement(' 1 0 0 '))
        zz
        >>> print(str_ints.decrement('- z '))
        -10
        >>> print(str_ints.decrement('-zz'))
        -100
        >>> print(str_ints.decrement('- 1'))
        -2
        >>> print(str_ints.decrement('0'))
        -1
        >>> print(str_ints.decrement('1'))
        0
        >>> print(str_ints.decrement('10000000000000000000000000000000000000000000000000000'))
        zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

        >>> str_ints = StrIntegers(8, True, 'abcdefgh')
        >>> print(str_ints.decrement(' B A A A '))
        hhh
        '''
        negative, value = self._prepare_crement_str_int(value)
        if value == self._str_zero:
            return u'-' + self._pos_int_to_str(1)
        if negative:
            result = self._increment_pos_str_int(value)
            if result == self._str_zero:
                return result
            return u'-' + result
        return self._decrement_pos_str_int(value)


# DECORATORS

def multi_decorator(*decorators):
    '''\
    Allows to create a decorator which applies a list of decorators to a
    target. The function returned applies the decorators in reverse order of
    ``decorators``, i.e. in the same order as decorators are written above
    their target.

    :param decorators: Each item must be a callable.
    :returns: a function which applies the decorators in reverse order of
        ``decorators``

    Examples:

    >>> def data_deco(name, data):
    ...     def decorator(target):
    ...         setattr(target, name, data)
    ...         return target
    ...     return decorator
    ...
    >>> metadata = multi_decorator(data_deco('title', 'Foo Bar'),
    ...     data_deco('content', 'Hello World!'))
    >>> @metadata
    ... class Data(object): pass
    >>> Data.title
    'Foo Bar'
    >>> Data.content
    'Hello World!'
    '''
    def decorator_func(target):
        for decorator in reversed(decorators):
            target = decorator(target)
        return target
    return decorator_func


class _NamespaceDict(dict):
    def __init__(self, original):
        self._original = original
        try:
            import builtins
            self._builtins = builtins
        except ImportError:
            self._builtins = __builtins__

    def __contains__(self, key):
        if dict.__contains__(self, key):
            return True
        return key in self._original

    def __len__(self):
        keys = set(dict.keys(self))
        keys.update(self._original.keys())
        return len(keys)

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            try:
                return self._original[key]
            except KeyError:
                return getattr(self._builtins, key)

    def get(self, key, default=None):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self._original.get(key, default)

    def keys(self):
        keys = set(dict.keys(self))
        keys.update(self._original.keys())
        for key in keys:
            yield key

    def items(self):
        for key in self:
            yield (key, self[key])

    def values(self):
        for key in self:
            yield self[key]

    __iter__ = keys

    if not PY_VERSION_GT_2:
        haskey = __contains__
        iter = keys
        iterkeys = keys
        iteritems = items
        itervalues = values

        def keys(self):
            return list(self.iterkeys())

        def items(self):
            return list(self.iteritems())

        def values(self):
            return list(self.itervalues())


def namespace(mapping, *names, **attributes):
    '''\
    Creates a function decorator which extends the namespace of the function
    it is applied to with entries from ``mapping``. Only global values are
    overridden.

    :arg mapping: The mapping containing namespace elements.
    :type mapping: mapping type
    :arg names: The names to define in the function namespace with values of
        the corresponding ``mapping`` entry. If none are given, all entries
        of ``mapping`` are added to the namespace (then it not only has to
        have the method :meth:`__getitem__` but must be a mapping conformant
        to :class:`collections.Mapping`).
    :param attributes: Named attributes which set entries on the namespace,
        possibly overriding entries from ``mappings``. The entry
        ``__staticglobals__`` is treated specially and does not define an
        entry on the namespace, for its meaning see below.
    :returns: The function decorator created.

    **Important:** If ``attributes`` contains an entry ``__staticglobals__``,
    this defines if the globals are to be treated static. If globals are
    treated static, in the decorated function only the state of the globals at
    definition time is available. Otherwise changes MAY be reflected in the
    function, but behavior for Python 2 is unspecified. For example in CPython
    2 dynamic globals are inaccessible, whereas it works in PyPy 2. In Python
    3 this works, as :class:`types.FunctionType` allows for arbitrary mappings
    to be used as globals. Thus the default for Python 2 is to use static
    globals for compatibility, in Python 3 the default is to use dynamic
    globals. To set the ``__staticglobals__`` entry of ``attributes`` to
    :const:`False` is the only way to archive predicatble behavior under
    Python 2 and 3 in all cases, otherwise be sure not modify entries in the
    global namespace after decorating the function.

    Examples:

    >>> class StringGenerator(object):
    ...     def __getitem__(self, name):
    ...         return 'StringGen: ' + name
    ...

    >>> a = 1
    >>> f = 'global'

    >>> @namespace(StringGenerator(), 'a', 'c', 'd', 'e', e='namespace e')
    ... def test(b, c=3):
    ...     print(a)
    ...     print(b)
    ...     print(c)
    ...     print(d)
    ...     print(e)
    ...     print(f)

    >>> test(2)
    StringGen: a
    2
    3
    StringGen: d
    namespace e
    global

    >>> @namespace(StringGenerator())
    ... def test():
    ...     print(a)
    ...
    Traceback (most recent call last):
    ValueError: The first argument must be a mapping.

    >>> @namespace(dict(a='namespace a', c='namespace c', d='namespace d'))
    ... def test(b, c=3):
    ...     print(a)
    ...     print(b)
    ...     print(c)
    ...     print(d)

    >>> test(2)
    namespace a
    2
    3
    namespace d
    '''
    if PY_VERSION_GT_2:
        staticglobals = bool(attributes.pop('__staticglobals__', False))
    else:
        staticglobals = bool(attributes.pop('__staticglobals__', True))
    def decorator(func):
        if staticglobals:
            func_globals = dict(func.__globals__)
        else:
            func_globals = _NamespaceDict(func.__globals__)
        try:
            if len(names) > 0:
                for name in names:
                    func_globals[name] = mapping[name]
            else:
                for name in mapping:
                    func_globals[name] = mapping[name]
        except TypeError:
            raise ValueError('The first argument must be a mapping.')
        try:
            func_closure = func.__closure__
        except AttributeError:
            func_closure = func.func_closure
        for name in attributes:
            func_globals[name] = attributes[name]
        from types import FunctionType
        return FunctionType(func.__code__, func_globals, func.__name__,
            func.__defaults__, func_closure)
    return decorator


def update_globals(**additional_entries):
    '''\
    Returns a function decorator which updates the globals of the function it
    is applied to with the entries from ``additional_entries``.

    :param additional_entries: The entries to update the globals with. The
        entry ``__staticglobals__`` is treated specially and does not define
        an entry on the namespace, for its meaning see below.
    :returns: The function decorator created.

    **Important:** If ``additional_entries`` contains an entry
    ``__staticglobals__``, this defines if the globals are to be treated
    static. If globals are treated static, in the decorated function only the
    state of the globals at definition time is available. Otherwise changes
    MAY be reflected in the function, but behavior for Python 2 is
    unspecified. For example in CPython 2 dynamic globals are inaccessible,
    whereas it works in PyPy 2. In Python 3 this works, as
    :class:`types.FunctionType` allows for arbitrary mappings to be used as
    globals. Thus the default for Python 2 is to use static globals for
    compatibility, in Python 3 the default is to use dynamic globals. To set
    the ``__staticglobals__`` entry of ``additional_entries`` to
    :const:`False` is the only way to archive predicatble behavior under
    Python 2 and 3 in all cases, otherwise be sure not modify entries in the
    global namespace after decorating the function.

    Example:

    >>> foo = 0
    >>> bar = 1
    >>> @update_globals(foo=-1)
    ... def foobar():
    ...     print(foo)
    ...     print(bar)

    >>> foobar()
    -1
    1
    '''
    if PY_VERSION_GT_2:
        staticglobals = bool(
            additional_entries.pop('__staticglobals__', False))
    else:
        staticglobals = bool(
            additional_entries.pop('__staticglobals__', True))
    from types import FunctionType
    def decorator(func):
        if staticglobals:
            new_globals = dict(func.__globals__)
        else:
            new_globals = _NamespaceDict(func.__globals__)
        new_globals.update(additional_entries)
        return FunctionType(func.__code__, new_globals, func.__name__)
    return decorator


def attribute_dict(target):
    '''\
    A decorator to create :class:`AttributeDict` instances from callables
    return values.

    :param target: The callable to be wrapped.
    :returns: A function which wraps ``target`` and returns an
        :class:`AttributeDict` from the return value of ``target``.

    Example:

    >>> @attribute_dict
    ... def Test(z):
    ...     def t(foo):
    ...         print(z)
    ...         print(foo)
    ...     return locals()
    ...
    >>> t = Test('foo')
    >>> t.z
    'foo'
    >>> t.t('bar')
    foo
    bar
    '''
    def wrapper(*args, **kargs):
        return AttributeDict(target(*args, **kargs))
    return wrapper



# SAX

class LexicalHandler(object):
    '''\
    A stub base class for a lexical handler (see
    :const:`xml.sax.handler.property_lexial_handler`).
    '''
    __metaclass__ = abc.ABCMeta

    def comment(self, content):
        '''Receive notification of a comment.'''
        pass

    def startCDATA(self):
        '''Receive notification of the beginning of CDATA section.'''
        pass

    def endCDATA(self):
        '''Receive notification of the end of CDATA section.'''
        pass


class DeclarationHandler(object):
    '''\
    A stub base class for a declaration handler (see
    :const:`xml.sax.handler.property_declaration_handler`).
    '''
    __metaclass__ = abc.ABCMeta

    def startDTD(self, name, public_id, system_id):
        '''Receive notification of the beginning of a DTD.'''
        pass

    def endDTD(self):
        '''Receive notification of the end of a DTD.'''
        pass

    def startEntity(self, name):
        '''Receive notification of the beginning of an entity.'''
        pass

    def endEntity(self, name):
        '''Receive notification of the end of an entity.'''
        pass

del abc