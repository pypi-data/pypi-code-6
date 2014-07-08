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

import collections
import inflection
import itertools
import operator

__all__ = ['Fake', 'Mock']


class Fake(object):
    """A fake is an object instantiated from its properties.

    Fakes are very useful in tests. They allow testers to instantiate objects from their properties in just one line,
    thus being an elegant way to create data structures on fly.

    Here is how to get a new fake :

    >>> from mocki.core import Fake
    >>>
    >>> fake = Fake(property='value', otherProperty='otherValue')

    This new fake takes the properties given on instantiation :

    >>> fake.property
    'value'
    >>>
    >>> fake.otherProperty
    'otherValue'

    """
    def __init__(self, **properties):
        self.__dict__.update(**properties)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Fake(%s)' % ', '.join(['%s=%r' % item for item in sorted(self.__dict__.items())])


class Mock(object):
    """A mock is a callable object that keeps track of any call invocation made from it.

    Here is how to get a new mock :

    >>> from mocki.core import Mock
    >>>
    >>> mock = Mock('theMock')

    It must be noted that mocks' members are mocks themselves :

    >>> mock.theMember # doctest: +ELLIPSIS
    <mocki.core.Mock object at ...>
    >>>
    >>> mock.theOtherMember # doctest: +ELLIPSIS
    <mocki.core.Mock object at ...>

    These new mocks take their names from the accessed members' names plus the name of the parent mock as follows :

    >>> mock.theMember.name
    'theMock.theMember'

    An important thing to note about mocks' members is that any member got from a parent mock under the same name is the
    same member :

    >>> mock.theMember is mock.theMember
    True

    """
    def __init__(self, name):
        from mocki import matchers

        self.name = name

        self.members = {}

        self.call_invocations = []
        self.verified_indices = []

        self.stub = lambda call_invocation: None

        self.builtin_matchers = {name: matchers.__dict__[name] for name in matchers.__all__}

    def __getattr__(self, name):
        if name.startswith('on_'):
            for matcher_name, matcher in self.builtin_matchers.items():
                if name == 'on_%s' % inflection.underscore(matcher_name):
                    return lambda *args, **kwargs: self.on(matcher(*args, **kwargs))

        if name.startswith('verify_'):
            for matcher_name, matcher in self.builtin_matchers.items():
                if name == 'verify_%s' % inflection.underscore(matcher_name):
                    return lambda *args, **kwargs: self.verify(matcher(*args, **kwargs))

        if not name in self.members:
            member = Mock('%s.%s' % (self.name, name))

            member.call_invocations = self.call_invocations
            member.verified_indices = self.verified_indices

            self.members[name] = member

        return self.members[name]

    def __call__(self, *args, **kwargs):
        call_invocation = CallInvocation(self, args, kwargs)

        self.call_invocations.append(call_invocation)

        return self.stub(call_invocation)

    @property
    def all_members(self):
        return list(itertools.chain(*[[member] + member.all_members for member in self.members.values()]))

    def get_call_invocation_history(self, matcher):
        call_invocations_with_indices = [
            (index, call_invocation) for index, call_invocation in enumerate(self.call_invocations)

            if call_invocation.mock is self
        ]

        call_invocations = list(map(operator.itemgetter(1), call_invocations_with_indices))

        matching_indices = [
            index for index, call_invocation in enumerate(call_invocations) if matcher(call_invocation)
        ]

        return CallInvocationHistory(call_invocations, matching_indices)

    def get_in_order_call_invocation_history(self, matcher, considered_mocks):
        call_invocations_with_indices = [
            (index, call_invocation) for index, call_invocation in enumerate(self.call_invocations)

            if (call_invocation.mock is self and matcher(call_invocation)) or any(map(
                lambda considered_mock: call_invocation.mock is considered_mock or any(map(
                    lambda member: call_invocation.mock is member,

                    considered_mock.all_members
                )),

                considered_mocks
            ))
        ]

        call_invocations = list(map(operator.itemgetter(1), call_invocations_with_indices))

        matching_indices = [
            index for index, call_invocation in enumerate(call_invocations) if matcher(call_invocation)
        ]

        verified_indices = [
            adjusted_index for adjusted_index, index
            in enumerate(map(operator.itemgetter(0), call_invocations_with_indices))

            if index in self.verified_indices
        ]

        return InOrderCallInvocationHistory(call_invocations, matching_indices, verified_indices)

    def get_no_more_call_invocation_history(self):
        call_invocations_with_indices = [
            (index, call_invocation) for index, call_invocation in enumerate(self.call_invocations)

            if call_invocation.mock is self or any(map(
                lambda member: call_invocation.mock is member,

                self.all_members
            ))
        ]

        call_invocations = list(map(operator.itemgetter(1), call_invocations_with_indices))

        verified_indices = [
            adjusted_index for adjusted_index, index
            in enumerate(map(operator.itemgetter(0), call_invocations_with_indices))

            if index in self.verified_indices
        ]

        return NoMoreCallInvocationHistory(call_invocations, verified_indices)

    def on(self, matcher):
        """Installs a new stub to change the mock's behavior.

        Suppose we have the following mock :

        >>> from mocki.core import Mock
        >>>
        >>> mock = Mock('theMock')

        By default, any call invoked from this mock returns nothing :

        >>> mock('1stCall')

        This behavior can be changed as follows :

        >>> mock.on(
        ...     lambda call_invocation: call_invocation.args == ('2ndCall',)
        ... ).do(
        ...     lambda call_invocation: '2ndValue'
        ... )

        A custom stub is now installed on the mock, such as any call invocation made from it by passing '2ndCall' will
        now return '2ndValue' :

        >>> mock('2ndCall')
        '2ndValue'

        Note that any other call invocation still returns nothing :

        >>> mock('1stCall')

        Here are some explanations.

        The statement used to install custom stubs is the following :
            mock.on(matcher).do(action)

        The matcher is a filter that describes on which call the stub will be applied. More concretely, it is a function
        taking a call invocation and returning true or false depending on whether this call invocation is suitable or
        not with the call we would like to stub. In our example, only call invocations made by passing '2ndCall' will be
        affected.

        The action is the function that will be executed whenever the matcher returns true. In our example, we simply
        returns '2ndValue'.

        It works well, but you may here wonder why we should write such a verbose stubbing statement for such a simple
        stub. It was to show you the fully customizable form of the stubbing statement, but of course, Mocki is shipped
        with a set of common matchers and actions, thus the above statement is strictly equivalent to the following
        one :

        >>> mock.on_call('2ndCall').do_return('2ndValue')

        That's much simpler !

        Another interesting thing to note about stubs is that they may also be partially overridden. This is done by
        declaring the more specific stub after the general one to override :

        >>> mock.on_any_call().do_return('defaultValue')
        >>>
        >>> mock.on_call('2ndCall').do_return('2ndValue')

        Now, any call invoked from this mock will return 'defaultValue', except for those made by passing '2ndCall'
        which will return '2ndValue' :

        >>> mock('1stCall')
        'defaultValue'
        >>>
        >>> mock('2ndCall')
        '2ndValue'
        >>>
        >>> mock('3rdCall')
        'defaultValue'

        """
        return PartialStubbing(self, matcher)

    def verify(self, matcher):
        """Verifies if a given call was invoked as expected from the given mock.

        If the given call was invoked as expected from the mock, this function just returns silently, otherwise it
        raises an exception indicating which call invocations are matching to the given call and which ones are not.

        Suppose we made the following call invocations :

        >>> from mocki.core import Mock
        >>>
        >>> mock = Mock('theMock')
        >>>
        >>> mock('1stCall')
        >>> mock('2ndCall')
        >>> mock('3rdCall')

        Let's verify if the 2nd call was invoked once :

        >>> mock.verify(
        ...     lambda call_invocation: call_invocation.args == ('2ndCall',)
        ... ).invoked(
        ...     lambda call_invocations: len(call_invocations) == 1
        ... )

        Here are some explanations.

        The statement used to do custom verifications is the following :
            mock.verify(matcher).invoked(expectation)

        The matcher is a filter that describes the call. More concretely, it is a function taking a call invocation and
        returning true or false depending on whether it is suitable or not with the given call, which is used to filter
        the call invocations made from the mock.

        The expectation is an assertion applied to the filtered call invocations that describes what is expected about
        the given call. It is a function taking the filtered call invocations and returning true or false depending on
        whether they meet or not the assertion.

        It works well, but you may here wonder why we should write such a verbose verification statement for such a
        simple assertion. It was to show you the fully customizable form of the verification statement, but of course,
        Mocki is shipped with a set of common matchers and expectations, thus the above statement is strictly equivalent
        to the following one :

        >>> mock.verify_call('2ndCall').invoked_once()

        Now, let's try to verify something wrong :

        >>> mock.verify_call('2ndCall').invoked_never()
        Traceback (most recent call last):
        ...
        AssertionError: Found one matching call invoked from theMock :
          theMock('1stCall')
        > theMock('2ndCall')
          theMock('3rdCall')

        An assertion error is raised along with a message in which matching call invocations are spotted by arrows. Here
        we found one matching call invocation while none was expected.

        Sometimes, it can be useful to verify whether or not a particular call was made in a particular order. This can
        be done using the in order verification statement.

        An important thing to note about this statement is that it can only be used from mocks that are sharing the same
        parent. This is not a real problem though, since mocks can easily be instantiated from other mocks :

        >>> new_mock, new_other_mock = mock.theNewMock, mock.theNewOtherMock

        Suppose we made the following call invocations :

        >>> new_mock('1stCall')
        >>> new_other_mock('2ndCall')
        >>> new_mock('3rdCall')
        >>> new_other_mock('4thCall')

        Then, we made the following verification :

        >>> new_other_mock.verify_call('2ndCall').invoked_once()

        Now, let's verify if the 1st call was invoked in order :

        >>> new_mock.verify_call('1stCall').invoked_in_order(new_other_mock)
        Traceback (most recent call last):
        ...
        AssertionError: Found one matching call invoked from theMock.theNewMock, but not in order :
          > theMock.theNewMock('1stCall')
        X   theMock.theNewOtherMock('2ndCall')
            theMock.theNewOtherMock('4thCall')

        An assertion error is raised along with a message in which matching call invocations are spotted by arrows while
        already verified ones are spotted by marks. Here we found one matching call invocation, but not in order : the
        2nd call has already been verified, which means that it was expected to be invoked before.

        Here are some explanations.

        The statement used to do custom in order verifications is the following :
            mock.verify(matcher).invoked_in_order(considered_mocks)

        The matcher is a filter that describes the call. More concretely, it is a function taking a call invocation and
        returning true or false depending on whether it is suitable or not with the given call, which is used to filter
        the call invocations made from the mock.

        The considered mocks are the mocks on which the statement applies. If at least one call invocation coming from
        these mocks was expected to be invoked after, the statement will fail.

        If the verified call was invoked in order, this function just returns silently :

        >>> new_mock.verify_call('3rdCall').invoked_in_order(new_other_mock)

        """
        return PartialVerification(self, matcher)

    def verify_no_more_call_invoked(self):
        """Verifies if there was no more call invoked from the given mock.

        If there was no more call invoked from the given mock, this function just returns silently, otherwise it raises
        an exception indicating which call invocations were already verified and which ones were not.

        Suppose we made the following call invocations :

        >>> from mocki.core import Mock
        >>>
        >>> mock = Mock('theMock')
        >>>
        >>> mock('1stCall')
        >>> mock('2ndCall')
        >>> mock('3rdCall')

        Then we made the following verifications :

        >>> mock.verify_call('1stCall').invoked_once()
        >>> mock.verify_call('3rdCall').invoked_once()

        If we now ask to verify if there was no more call invoked from this mock, an assertion error is raised along
        with a message in which already verified call invocations are spotted by marks :

        >>> mock.verify_no_more_call_invoked()
        Traceback (most recent call last):
        ...
        AssertionError: Found one call invoked from theMock that was not verified :
        X theMock('1stCall')
          theMock('2ndCall')
        X theMock('3rdCall')

        We can see that one call invocation was not verified. So let's verify it :

        >>> mock.verify_call('2ndCall').invoked_once()

        Now, this function just returns silently :

        >>> mock.verify_no_more_call_invoked()

        It must be noted that any call invoked from mock's members is here taken into account, which explains why we get
        an assertion error once again when we invoke some calls from them :

        >>> mock.theMember('4thCall')
        >>>
        >>> mock.verify_no_more_call_invoked()
        Traceback (most recent call last):
        ...
        AssertionError: Found one call invoked from theMock that was not verified :
        X theMock('1stCall')
        X theMock('2ndCall')
        X theMock('3rdCall')
          theMock.theMember('4thCall')

        """
        do_no_more_verification(self)


class PartialStubbing(object):
    def __init__(self, mock, matcher):
        from mocki import actions

        self.mock, self.matcher = mock, matcher

        self.builtin_actions = {name: actions.__dict__[name] for name in actions.__all__}

    def __getattr__(self, name):
        if name.startswith('do_'):
            for action_name, action in self.builtin_actions.items():
                if name == 'do_%s' % inflection.underscore(action_name):
                    return lambda *args, **kwargs: self.do(action(*args, **kwargs))

        raise AttributeError('%r has no attribute %r' % (self, name))

    def do(self, action):
        self.mock.stub = Stub(self.matcher, action, self.mock.stub)


class Stub(object):
    def __init__(self, matcher, action, next_stub):
        self.matcher, self.action, self.next_stub = matcher, action, next_stub

    def __call__(self, call_invocation):
        if self.matcher(call_invocation):
            return self.action(call_invocation)
        else:
            return self.next_stub(call_invocation)


class PartialVerification(object):
    def __init__(self, mock, matcher):
        from mocki import expectations

        self.mock, self.matcher = mock, matcher

        self.builtin_expectations = {name: expectations.__dict__[name] for name in expectations.__all__}

    def __getattr__(self, name):
        if name.startswith('invoked_'):
            for expectation_name, expectation in self.builtin_expectations.items():
                if name == 'invoked_%s' % inflection.underscore(expectation_name):
                    return lambda *args, **kwargs: self.invoked(expectation(*args, **kwargs))

        raise AttributeError('%r has no attribute %r' % (self, name))

    def invoked(self, expectation):
        do_verification(self.mock, self.matcher, expectation)

    def invoked_in_order(self, *considered_mocks):
        do_in_order_verification(self.mock, self.matcher, considered_mocks)


def do_verification(mock, matcher, expectation):
    call_invocation_history = mock.get_call_invocation_history(matcher)

    if expectation(call_invocation_history.matching_call_invocations):
        mock.verified_indices.extend([
            index for index, call_invocation in enumerate(mock.call_invocations)

            if matcher(call_invocation)
        ])
    else:
        if len(call_invocation_history.call_invocations) == 0:
            raise AssertionError('No call invoked from {mock_name}.'.format(
                mock_name=mock.name,
            ))

        if len(call_invocation_history.matching_indices) == 0:
            raise AssertionError('Found no matching call invoked from {mock_name} :'.format(
                mock_name=mock.name,

            ) + '\n' + print_call_invocation_history(call_invocation_history))

        if len(call_invocation_history.matching_indices) == 1:
            raise AssertionError('Found one matching call invoked from {mock_name} :'.format(
                mock_name=mock.name,

            ) + '\n' + print_call_invocation_history(call_invocation_history))

        if len(call_invocation_history.matching_indices) > 1:
            raise AssertionError('Found {nb_calls} matching calls invoked from {mock_name} :'.format(
                nb_calls=len(call_invocation_history.matching_indices), mock_name=mock.name,

            ) + '\n' + print_call_invocation_history(call_invocation_history))


def do_in_order_verification(mock, matcher, considered_mocks):
    call_invocation_history = mock.get_in_order_call_invocation_history(matcher, considered_mocks)

    if call_invocation_history.in_order_matching_indices:
        mock.verified_indices.append(min([
            index for index, call_invocation in enumerate(mock.call_invocations)

            if matcher(call_invocation) and index > (max(mock.verified_indices) if mock.verified_indices else 0)
        ]))
    else:
        if len(call_invocation_history.call_invocations) == 0:
            raise AssertionError('No call invoked from {mock_name}.'.format(
                mock_name=mock.name,
            ))

        if len(call_invocation_history.matching_indices) == 0:
            raise AssertionError('Found no matching call invoked from {mock_name} :'.format(
                mock_name=mock.name,

            ) + '\n' + print_in_order_call_invocation_history(call_invocation_history))

        if len(call_invocation_history.matching_indices) == 1:
            raise AssertionError('Found one matching call invoked from {mock_name}, but not in order :'.format(
                mock_name=mock.name,

            ) + '\n' + print_in_order_call_invocation_history(call_invocation_history))

        if len(call_invocation_history.matching_indices) > 1:
            raise AssertionError('Found {nb_calls} matching calls invoked from {mock_name}, but not in order :'.format(
                nb_calls=len(call_invocation_history.matching_indices), mock_name=mock.name,

            ) + '\n' + print_in_order_call_invocation_history(call_invocation_history))


def do_no_more_verification(mock):
    call_invocation_history = mock.get_no_more_call_invocation_history()

    if len(call_invocation_history.non_verified_indices) == 1:
        raise AssertionError('Found one call invoked from {mock_name} that was not verified :'.format(
            mock_name=mock.name,

        ) + '\n' + print_no_more_call_invocation_history(call_invocation_history))

    if len(call_invocation_history.non_verified_indices) > 1:
        raise AssertionError('Found {nb_calls} calls invoked from {mock_name} that was not verified :'.format(
            nb_calls=len(call_invocation_history.non_verified_indices), mock_name=mock.name,

        ) + '\n' + print_no_more_call_invocation_history(call_invocation_history))


class CallInvocationHistory(object):
    def __init__(self, call_invocations, matching_indices):
        self.call_invocations, self.matching_indices = (
            call_invocations, matching_indices
        )

    @property
    def matching_call_invocations(self):
        return [self.call_invocations[index] for index in self.matching_indices]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


def print_call_invocation_history(call_invocation_history):
    history_lines_strs = []

    for index, call_invocation in enumerate(call_invocation_history.call_invocations):
        if index in call_invocation_history.matching_indices:
            history_lines_strs.append('> %s' % print_call_invocation(call_invocation))
        else:
            history_lines_strs.append('  %s' % print_call_invocation(call_invocation))

    return '\n'.join(history_lines_strs)


class InOrderCallInvocationHistory(object):
    def __init__(self, call_invocations, matching_indices, verified_indices):
        self.call_invocations, self.matching_indices, self.verified_indices = (
            call_invocations, matching_indices, verified_indices
        )

    @property
    def matching_call_invocations(self):
        return [self.call_invocations[index] for index in self.matching_indices]

    @property
    def verified_call_invocations(self):
        return [self.call_invocations[index] for index in self.verified_indices]

    @property
    def in_order_matching_indices(self):
        if self.verified_indices:
            return [index for index in self.matching_indices if index > max(self.verified_indices)]
        else:
            return self.matching_indices

    @property
    def in_order_matching_call_invocations(self):
        return [self.call_invocations[index] for index in self.in_order_matching_indices]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


def print_in_order_call_invocation_history(call_invocation_history):
    history_lines_strs = []

    for index, call_invocation in enumerate(call_invocation_history.call_invocations):
        if index in call_invocation_history.matching_indices:
            if index in call_invocation_history.verified_indices:
                history_lines_strs.append('X > %s' % print_call_invocation(call_invocation))
            else:
                history_lines_strs.append('  > %s' % print_call_invocation(call_invocation))
        else:
            if index in call_invocation_history.verified_indices:
                history_lines_strs.append('X   %s' % print_call_invocation(call_invocation))
            else:
                history_lines_strs.append('    %s' % print_call_invocation(call_invocation))

    return '\n'.join(history_lines_strs)


class NoMoreCallInvocationHistory(object):
    def __init__(self, call_invocations, verified_indices):
        self.call_invocations, self.verified_indices = (
            call_invocations, verified_indices
        )

    @property
    def verified_call_invocations(self):
        return [self.call_invocations[index] for index in self.verified_indices]

    @property
    def non_verified_indices(self):
        return [index for index in range(len(self.call_invocations)) if index not in self.verified_indices]

    @property
    def non_verified_call_invocations(self):
        return [self.call_invocations[index] for index in self.non_verified_indices]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


def print_no_more_call_invocation_history(call_invocation_history):
    history_lines_strs = []

    for index, call_invocation in enumerate(call_invocation_history.call_invocations):
        if index in call_invocation_history.verified_indices:
            history_lines_strs.append('X %s' % print_call_invocation(call_invocation))
        else:
            history_lines_strs.append('  %s' % print_call_invocation(call_invocation))

    return '\n'.join(history_lines_strs)


CallInvocation = collections.namedtuple('CallInvocation', 'mock args kwargs')


def print_call_invocation(call_invocation):
    args, kwargs = call_invocation.args, sorted(call_invocation.kwargs.items())

    if args and kwargs:
        return '{mock_name}({args}, {kwargs})'.format(
            mock_name=call_invocation.mock.name,

            args=', '.join(['%r' % arg for arg in args]),
            kwargs=', '.join(['%s=%r' % kwarg for kwarg in kwargs]),
        )
    elif args:
        return '{mock_name}({args})'.format(
            mock_name=call_invocation.mock.name,

            args=', '.join(['%r' % arg for arg in args]),
        )
    elif kwargs:
        return '{mock_name}({kwargs})'.format(
            mock_name=call_invocation.mock.name,

            kwargs=', '.join(['%s=%r' % kwarg for kwarg in kwargs]),
        )
    else:
        return '{mock_name}()'.format(
            mock_name=call_invocation.mock.name,
        )
