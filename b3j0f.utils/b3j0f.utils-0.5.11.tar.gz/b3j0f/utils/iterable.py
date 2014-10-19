# -*- coding: utf-8 -*-

from collections import Iterable


def isiterable(element, exclude=None):
    """
    Check whatever or not if input element is an iterable.

    :param element: element to check among iterable types.
    :param type/tuple exclude: not allowed types in the test.

    >>> isiterable({})
    True
    >>> isiterable({}, exclude=dict)
    False
    >>> isiterable({}, exclude=(dict,))
    False
    """

    # check for allowed type
    allowed = exclude is None or not isinstance(element, exclude)
    result = allowed and isinstance(element, Iterable)

    return result


def ensureiterable(value, iterable=list, exclude=None):
    """
    Convert a value into an iterable if it is not.

    :param object value: object to convert
    :param type iterable: iterable type to apply (default: list)
    :param type/tuple exclude: types to not convert
    """

    result = value

    if not isiterable(value, exclude=exclude):
        result = [value]
        result = iterable(result)

    else:
        result = iterable(value)

    return result


def first(iterable, default=None):
    """
    Try to get input iterable first item or default if iterable is empty.

    :param Iterable iterable: iterable to iterate on.
    :param default: default value to get if input iterable is empty.
    :raises TypeError: if iterable is not an iterable value
    """

    # start to get the iterable iterator (raises TypeError if iter)
    iterator = iter(iterable)
    # get first element
    try:
        result = next(iterator)
    except StopIteration:
        # if no element exist, result equals default
        result = default

    return result
