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

__all__ = ['Return', 'Raise', 'InOrder']


class Return(object):
    """An action that returns the given value.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    Here is how to stub this mock to return a value :

    >>> mock.on_any_call().do_return('value')

    Now, any call invocation made from it will return this value :

    >>> mock('1stCall')
    'value'

    """
    def __init__(self, value):
        self.value = value

    # noinspection PyUnusedLocal
    def __call__(self, call_invocation):
        return self.value


class Raise(object):
    """An action that raises the given exception.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    Here is how to stub this mock to raise an exception :

    >>> mock.on_any_call().do_raise(Exception('error'))

    Now, any call invocation made from it will raise this exception :

    >>> mock('1stCall')
    Traceback (most recent call last):
    ...
    Exception: error

    """
    def __init__(self, exception):
        self.exception = exception

    def __call__(self, call_invocation):
        raise self.exception


class InOrder(object):
    """An action that takes a list of actions to execute in order.

    The 1st action will be executed on the 1st matching call invocation, the 2nd action on the 2nd one, the 3rd action
    on the 3rd one, and so on, up to the last action that will be repeatedly executed on any further matching call
    invocation.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    Here is an example showing how to stub this mock with a list of actions :

    >>> mock.on_any_call().do_in_order(Return('value'), Return('otherValue'))

    With this stub installed, the 1st call invocation made from the mock will now return 'value', while any further one
    will return 'otherValue' :

    >>> mock('1stCall')
    'value'
    >>>
    >>> mock('2ndCall')
    'otherValue'
    >>>
    >>> mock('3rdCall')
    'otherValue'

    """
    def __init__(self, stub, *stubs):
        self.stubs = [stub] + list(stubs)

        self.stubs_iter = iter(self.stubs)

    def __call__(self, call_invocation):
        try:
            return next(self.stubs_iter)(call_invocation)
        except StopIteration:
            return self.stubs[-1](call_invocation)
