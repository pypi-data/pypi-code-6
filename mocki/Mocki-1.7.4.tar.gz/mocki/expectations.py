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

__all__ = ['AtLeast', 'AtLeastOnce', 'AtMost', 'AtMostOnce', 'Between', 'Exactly', 'Never', 'Once']


class AtLeast(object):
    """An expectation that returns true when there is at least N matching call invocations.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if it was invoked at least 1 time :

    >>> mock.verify_any_call().invoked_at_least(1)
    Traceback (most recent call last):
    ...
    AssertionError: No call invoked from theMock.

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_at_least(1)

    With 2 calls invoked :

    >>> mock('2ndCall')
    >>>
    >>> mock.verify_any_call().invoked_at_least(1)

    """
    def __init__(self, n_times):
        self.n_times = n_times

    def __call__(self, call_invocations):
        return len(call_invocations) >= self.n_times


class AtLeastOnce(object):
    """An expectation that returns true when there is at least one matching call invocation.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if is was invoked at least once :

    >>> mock.verify_any_call().invoked_at_least_once()
    Traceback (most recent call last):
    ...
    AssertionError: No call invoked from theMock.

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_at_least_once()

    With 2 calls invoked :

    >>> mock('2ndCall')
    >>>
    >>> mock.verify_any_call().invoked_at_least_once()

    """
    def __call__(self, call_invocations):
        return len(call_invocations) >= 1


class AtMost(object):
    """An expectation that returns true when there is at most N matching call invocations.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if it was invoked at most 1 time :

    >>> mock.verify_any_call().invoked_at_most(1)

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_at_most(1)

    With 2 calls invoked :

    >>> mock('2ndCall')
    >>>
    >>> mock.verify_any_call().invoked_at_most(1)
    Traceback (most recent call last):
    ...
    AssertionError: Found 2 matching calls invoked from theMock :
    > theMock('1stCall')
    > theMock('2ndCall')

    """
    def __init__(self, n_times):
        self.n_times = n_times

    def __call__(self, call_invocations):
        return len(call_invocations) <= self.n_times


class AtMostOnce(object):
    """An expectation that returns true when there is at most one matching call invocation.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if it was invoked at most once :

    >>> mock.verify_any_call().invoked_at_most_once()

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_at_most_once()

    With 2 calls invoked :

    >>> mock('2ndCall')
    >>>
    >>> mock.verify_any_call().invoked_at_most_once()
    Traceback (most recent call last):
    ...
    AssertionError: Found 2 matching calls invoked from theMock :
    > theMock('1stCall')
    > theMock('2ndCall')

    """
    def __call__(self, call_invocations):
        return len(call_invocations) <= 1


class Between(object):
    """An expectation that returns true when there is between N and M matching call invocations.

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if it was invoked between 1 and 3
    times :

    >>> mock.verify_any_call().invoked_between(1, 3)
    Traceback (most recent call last):
    ...
    AssertionError: No call invoked from theMock.

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_between(1, 3)

    With 2 calls invoked :

    >>> mock('2ndCall')
    >>>
    >>> mock.verify_any_call().invoked_between(1, 3)

    With 3 calls invoked :

    >>> mock('3rdCall')
    >>>
    >>> mock.verify_any_call().invoked_between(1, 3)

    With 4 calls invoked :

    >>> mock('4thCall')
    >>>
    >>> mock.verify_any_call().invoked_between(1, 3)
    Traceback (most recent call last):
    ...
    AssertionError: Found 4 matching calls invoked from theMock :
    > theMock('1stCall')
    > theMock('2ndCall')
    > theMock('3rdCall')
    > theMock('4thCall')

    """
    def __init__(self, n_times, m_times):
        self.n_times, self.m_times = n_times, m_times

    def __call__(self, call_invocations):
        return self.n_times <= len(call_invocations) <= self.m_times


class Exactly(object):
    """An expectation that returns true when there is exactly N matching call invocations.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if it was invoked exactly 1 time :

    >>> mock.verify_any_call().invoked_exactly(1)
    Traceback (most recent call last):
    ...
    AssertionError: No call invoked from theMock.

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_exactly(1)

    With 2 calls invoked :

    >>> mock('2ndCall')
    >>>
    >>> mock.verify_any_call().invoked_exactly(1)
    Traceback (most recent call last):
    ...
    AssertionError: Found 2 matching calls invoked from theMock :
    > theMock('1stCall')
    > theMock('2ndCall')

    """
    def __init__(self, n_times):
        self.n_times = n_times

    def __call__(self, call_invocations):
        return len(call_invocations) == self.n_times


class Never(object):
    """An expectation that returns true when there is no matching call invocation.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if it was never invoked :

    >>> mock.verify_any_call().invoked_never()

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_never()
    Traceback (most recent call last):
    ...
    AssertionError: Found one matching call invoked from theMock :
    > theMock('1stCall')

    """
    def __call__(self, call_invocations):
        return len(call_invocations) == 0


class Once(object):
    """An expectation that returns true when there is one matching call invocation.

    Suppose we have the following mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    With no call invoked from this mock, here is what we get when we ask to verify if it was invoked once :

    >>> mock.verify_any_call().invoked_once()
    Traceback (most recent call last):
    ...
    AssertionError: No call invoked from theMock.

    With one call invoked :

    >>> mock('1stCall')
    >>>
    >>> mock.verify_any_call().invoked_once()

    With 2 calls invoked :

    >>> mock('2ndCall')
    >>>
    >>> mock.verify_any_call().invoked_once()
    Traceback (most recent call last):
    ...
    AssertionError: Found 2 matching calls invoked from theMock :
    > theMock('1stCall')
    > theMock('2ndCall')

    """
    def __call__(self, call_invocations):
        return len(call_invocations) == 1
