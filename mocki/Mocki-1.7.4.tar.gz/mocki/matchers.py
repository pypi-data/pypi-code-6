#
#   Copyright 2011 Olivier Kozak
#
#   This file is part of Mocki.
#
#   Mocki is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
#   version.
#
#   Mocki is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License along with Mocki. If not, see
#   <http://www.gnu.org/licenses/>.
#

__all__ = ['AnyCall', 'Call']


class AnyCall(object):
    """A matcher that matches any call invocation.

    This matcher is usable either from verification or stubbing statements.

    Suppose we made the following call invocations :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')
    >>>
    >>> mock('1stCall')
    >>> mock('2ndCall')
    >>> mock('3rdCall')

    As we can see from the following verification statement, this matcher will match any call invoked from the mock :

    >>> mock.verify_any_call().invoked_once()
    Traceback (most recent call last):
    ...
    AssertionError: Found 3 matching calls invoked from theMock :
    > theMock('1stCall')
    > theMock('2ndCall')
    > theMock('3rdCall')

    In a stubbing statement, this matcher is used to constantly execute the same action, no matter what arguments were
    provided to invoke the call.

    Here is an example showing how to use it to stub the mock :

    >>> mock.on_any_call().do_return('value')

    With this stub installed, 'value' will now be constantly returned on any call invocation made from the mock :

    >>> mock('1stCall')
    'value'
    >>>
    >>> mock('2ndCall')
    'value'

    """
    # noinspection PyUnusedLocal
    def __call__(self, call_invocation):
        return True


class Call(object):
    """A matcher that matches call invocations made with the given arguments.

    This matcher is usable either from verification or stubbing statements.

    Suppose we made the following call invocations :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')
    >>>
    >>> mock('1stCall')
    >>> mock('2ndCall')
    >>> mock('2ndCall')
    >>> mock('3rdCall')

    As we can see from the following verification statement, this matcher will only match the calls invoked from the
    mock with the given arguments :

    >>> mock.verify_call('2ndCall').invoked_once()
    Traceback (most recent call last):
    ...
    AssertionError: Found 2 matching calls invoked from theMock :
      theMock('1stCall')
    > theMock('2ndCall')
    > theMock('2ndCall')
      theMock('3rdCall')

    In the previous verification statement, we used values for arguments. This is the most common situation, but
    sometimes, it may be useful to describe these arguments with richer assertions. This can be done using callables :

    >>> mock.verify_call(lambda value: value != '2ndCall').invoked_once()
    Traceback (most recent call last):
    ...
    AssertionError: Found 2 matching calls invoked from theMock :
    > theMock('1stCall')
      theMock('2ndCall')
      theMock('2ndCall')
    > theMock('3rdCall')

    We can also use the more expressive Hamcrest version :

    >>> from hamcrest import equal_to, is_not
    >>>
    >>> mock.verify_call(is_not(equal_to('2ndCall'))).invoked_once()
    Traceback (most recent call last):
    ...
    AssertionError: Found 2 matching calls invoked from theMock :
    > theMock('1stCall')
      theMock('2ndCall')
      theMock('2ndCall')
    > theMock('3rdCall')

    In a stubbing statement, this matcher is used to execute different actions on different call invocations.

    Here is an example showing how to use it to stub the mock :

    >>> mock.on_call('1stCall').do_return('value')
    >>> mock.on_call('3rdCall').do_return('otherValue')

    With this stub installed, 'value' will now be returned each time a call invocation is made from the mock by passing
    '1stCall', while 'otherValue' will be returned for those made by passing '3rdCall' :

    >>> mock('1stCall')
    'value'
    >>>
    >>> mock('3rdCall')
    'otherValue'

    """
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs

    def __call__(self, call_invocation):
        args = tuple([ArgPlaceholder(arg) for arg in self.args])
        kwargs = dict([(name, ArgPlaceholder(kwarg)) for name, kwarg in self.kwargs.items()])

        return (call_invocation.args, call_invocation.kwargs) == (args, kwargs)


class ArgPlaceholder(object):
    def __init__(self, expected_value):
        self.expected_value = expected_value

    def __eq__(self, value):
        if hasattr(self.expected_value, 'matches'):
            return self.expected_value.matches(value)
        elif hasattr(self.expected_value, '__call__'):
            return self.expected_value(value)
        else:
            return self.expected_value == value
