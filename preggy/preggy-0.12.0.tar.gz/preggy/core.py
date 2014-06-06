# -*- coding: utf-8 -*-
'''preggy core: the `Expect` class, and the `@assertion` and `@create_assertions` decorators.
'''
# preggy assertions
# https://github.com/heynemann/preggy

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Bernardo Heynemann heynemann@gmail.com

from __future__ import absolute_import
import functools

from preggy import utils

_registered_assertions = utils.AssertionsMap()


def assertion(func):
    '''Function decorator.  Provides lower-level control for custom
    assertions than `@preggy.create_assertions`.

    This decorator is preferable over `@preggy.create_assertions`
    if you need to fine-tune your error message, or if your assertion
    doesn’t have a corresponding `not_`.

    Unlike `@preggy.create_assertions`, functions decorated with
    this shouldn’t return a boolean. Instead, they should check for
    undesirable conditions and raise an `AssertionError` when appropriate.

    Whenever possible, you should declare both the normal assertion as well
    as a `not_` counterpart, so they can be used like this:
    
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    >>>
    >>> import preggy
    >>> from preggy.core import Expect as expect
    >>> 
    >>> @preggy.assertion
    ... def to_be_a_positive_integer(topic):
    ...     if not topic > 0:
    ...          raise AssertionError("Expected topic('{topic}') to be a positive integer".format(topic=topic))
    ...
    >>> @preggy.assertion
    ... def not_to_be_a_positive_integer(topic):
    ...     if not topic < 0:
    ...          raise AssertionError("Expected topic('{topic}') not to be a positive integer".format(topic=topic))
    ...
    >>> expect(5).to_be_a_positive_integer()
    >>> expect(-3).Not.to_be_a_positive_integer()

    '''
    if not hasattr(func, 'humanized'):
        setattr(func, 'humanized', utils.humanized_name(func.__name__))
        
    @functools.wraps(func)
    def wrapper(*args, **kw):
        return func(*args, **kw)

    _registered_assertions[wrapper.__name__] = wrapper
    return wrapper


def create_assertions(func):
    '''Function decorator.  Use to create custom assertions for your
    tests.
    ''' '''
    Creating new assertions for use with `expect` is as simple as using
    this decorator on a function. The function expects `topic` as the
    first parameter, and `expectation` second:

        @preggy.create_assertions
        def to_be_greater_than(topic, expected):
            return topic > expected

    This creates both the assertion AND its `not_*` counterpart.  
    
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    >>> from preggy.core import (assertion, create_assertions, Expect as expect)  
    >>> from preggy.assertions import *
    
    >>> expect(2).to_be_greater_than(3)
    Traceback (most recent call last):
        ...
    AssertionError: Expected topic(2) to be greater than 3
    
    >>> expect(4).not_to_be_greater_than(3)
    Traceback (most recent call last):
        ...
    AssertionError: Expected topic(4) not to be greater than 3
    
    '''
    # set custom func attribute "humanized"
    setattr(func, 'humanized', utils.humanized_name(func.__name__))

    # modified functools.update_wrapper
    def _update_wrapper(wrapper, wrapped, not_assertion=True):
        '''A modified version of functools.update_wrapper. Auto-modifies the
        wrapper's __name__ and __doc__ to create a not_assertion.
        '''
        # begin as usual
        wrapper = functools.update_wrapper(wrapper, wrapped)
        
        # compute overrides for not_* assertions values
        if not_assertion:
            new_name = 'not_{0.__name__}'.format(wrapped)
            new_doc = ''#.format(wrapped)

            # set our overrides
            setattr(wrapper, '__name__', new_name)
            setattr(wrapper, '__doc__', new_doc)
            # update to reflect new __name__
            setattr(wrapper, 'humanized', utils.humanized_name(wrapper.__name__))

        # Return the wrapper so this can be used as a decorator via partial()
        return wrapper
    
    
    # First assertion
    @assertion
    @functools.wraps(func)
    def test_assertion(*args):
        raw_msg = utils.format_assertion_msg(func.humanized, *args)
        err_msg = raw_msg.format(*args)
        if not func(*args):
            raise AssertionError(err_msg)
    
    # Second assertion: prepare
    def test_not_assertion(*args):
        raw_msg = utils.format_assertion_msg('not {0!s}'.format(func.humanized), *args)
        err_msg = raw_msg.format(*args)
        if func(*args):
            raise AssertionError(err_msg)

    # Second assertion: update and register
    test_not_assertion = _update_wrapper(test_not_assertion, func)
    test_not_assertion = assertion(test_not_assertion)


class Expect(object):
    '''This atypical class provides a key part of the preggy testing syntax.
    
    For example:
    
        >>> from preggy.core import (assertion, create_assertions, Expect as expect)
        >>> from preggy.assertions import *
        >>>
        >>> expect(True).to_be_true()
        >>> expect(False).to_be_false()
        
    '''

    def __init__(self, topic):
        self.topic = topic
        self.not_assert = False

    @classmethod
    def not_to_be_here(self):
        raise AssertionError("Should not have gotten this far.")

    def __getattr__(self, name):
        # common cases
        if name in ['topic', 'not_to_be_here']:
            return super(Expect, self).__getattr__(name)
        if name == 'Not':
            self.not_assert = not self.not_assert
            return self

        # determine whether assertion is of "not" form
        method_name = 'not_{name}'.format(name=name) if self.not_assert else name
        
        # if program gets this far, then it’s time to perform the assertion. (...FINALLY! ;D)
        def _assert_topic(*args, **kw):
            # Allows chained calls to assertions, such as `expect(topic).to_be_true()`.
            return _registered_assertions[method_name](self.topic, *args, **kw)
        
        return _assert_topic
