# -*- coding: utf-8 -*-
"""pyneric module

This module contains generic utility functions.

"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from pyneric.future import *

import keyword
import inspect
import re

from pyneric._version import __version__, __version_info__


__all__ = ['__version__', '__version_info__']


__all__.append('module_attributes')
def module_attributes(module, use_all=None, include_underscored=False):
    """Return a list of the attributes of the given module.

    The module's '__all__' attribute determines the result if `use_all` is true
    or it is None and the attribute is defined; otherwise, `dir` is used, and
    its results are filtered to exclude names starting with an underscore if
    `include_underscore` is false.

    Passing a true value for `use_all` is a convenience for the caller when it
    requires that the module shall have an '__all__' attribute and an exception
    shall be raised if it does not.

    """
    if use_all or use_all is None and hasattr(module, '__all__'):
        return list(module.__all__)
    result = dir(module)
    if include_underscored:
        return result
    return [x for x in result if not x.startswith('_')]


__all__.append('pascalize')
def pascalize(value, validate=True):
    """Return the conversion of the given string value to Pascal format."""
    result = re.sub('(?:^|_)(.)', lambda x: x.group(0)[-1].upper(), value)
    result_type = type(value)
    if type(result) is not result_type:
        result = result_type(result)
    return result


__all__.append('tryf')
# PY2 note: The definition would be the following in Python 3+:
# def tryf(func, *args, _except=Exception, _return=None, **kwargs):
def tryf(func, *args, **kwargs):
    """Wrap a function call in a try/except statement.

    The given function is called with the given arguments inside a try
    statement.  If the/any exception(s) specified in the `_except` argument
    occur(s), then the value specified in the `_return` argument is returned;
    otherwise, the result is the same as without this wrapper.

    If the wrapped function expects keyword arguments named '_except' or
    '_return', it will never receive them, so the try statement should be used
    for those instead of this function.

    """
    # PY2 note: The _except and _return assignments should be removed when the
    # function definition changes to Python 3+ syntax.
    _except = kwargs.pop('_except', Exception)
    _return = kwargs.pop('_return', None)
    try:
        return func(*args, **kwargs)
    except _except:
        return _return


__all__.append('underscore')
def underscore(value, validate=True, multicap=True):
    """Return the conversion of the given string value to variable format.

    This converts non-penultimate upper-case characters to lower-case preceded
    by an underscore.

    """
    if validate:
        valid_python_identifier(value, exception=True)
    patterns = ['[A-Z]']
    if multicap:
        patterns.insert(0, '[A-Z]+(?=($|[A-Z][a-z]))')
    pattern = '(' + '|'.join(patterns) + ')'
    result = re.sub(pattern, lambda x: "_" + x.groups()[0].lower(), value)[1:]
    result_type = type(value)
    if type(result) is not result_type:
        result = result_type(result)
    return result


__all__.append('valid_python_identifier')
def valid_python_identifier(value, dotted=False, exception=False):
    """Validate that the given string value is a valid Python identifier.

    The value is also validated as a non-keyword in Python.

    If `dotted` is true, then each string around any dots is validated.

    If `exception` is false, then return whether the value is valid; otherwise,
    if the value is valid, return True; otherwise, raise an `exception`
    instance if it is an exception class or `ValueError`, each instantiated
    with a string describing why the value is invalid.

    """
    if not isinstance(value, basestring):
        raise TypeError("{!r} is not a string.".format(value))
    if dotted:
        return all(valid_python_identifier(x, exception=exception)
                   for x in value.split('.'))
    problem = None
    if not future.isidentifier(value, dotted=dotted):
        problem = "is not a valid Python identifier"
    elif keyword.iskeyword(value):
        problem = "is a Python keyword"
    if not (problem and exception):
        return not problem
    if not (inspect.isclass(exception) and
            issubclass(exception, BaseException)):
        exception = ValueError
    raise exception("{!r} {}.".format(value, problem))
