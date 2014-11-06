"""
Copyright (C) 2014 Haak Saxberg

This file is part of Solid, a state machine package for Python.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import re

from solid.transition import Transition, END
from solid.util import ReadOnlyStateWrapper


class BaseState(object):

    IS_ENTRY_STATE = False

    def __init__(self, parent_machine):
        self._parent_machine = parent_machine

    @property
    def parent_machine(self):
        try:
            return self._parent_machine
        except AttributeError:
            return None

    @parent_machine.setter
    def parent_machine(self, value):
        if self.parent_machine is None:
            self._parent_machine = value
        else:
            raise AttributeError(
                "Can't reset parent_machine on {}".format(self),
            )

    @property
    def previous_state(self):
        """read-only wrapper for use in on_entry"""
        try:
            return ReadOnlyStateWrapper(self._previous_state)
        except AttributeError:
            return None

    @property
    def next_state(self):
        """read-only wrapper for use in on_exit"""
        try:
            return ReadOnlyStateWrapper(self._next_state)
        except AttributeError:
            return None

    @classmethod
    def get_instance_attr_name(cls):
        """Transforms a ClassName into a more readable function_name, so that
        it feels less gross to call a machine's entry states like functions.

        Subclasses can obviously override to change this behavior."""
        return re.sub('(?!^)([A-Z]+)', r'_\1', cls.__name__).lower()

    def on_entry(self, transition):
        """Function that gets executed as the machine enters this state.

        Args:
            transition --- how we got here """
        pass

    def do_body(self, previous_transition):
        return self.body(**previous_transition.kwargs)

    def body(self, **body_args):
        """do the work of the state. subclasses must implement this method.

        should return a Transition object or None, inidicating the next state
        and what arguments it should receive. If the return value is None,
        indicates that this is a terminating state."""
        raise NotImplementedError()

    def on_exit(self, expected_transition):
        """Function that executes as the machine leaves this state.

        This function should return None or a State --- if not None, the return
        value will be used as the next state in the machine's run.

        Args:
            expected_transition --- where the machine is going to go
        """
        pass

    def run(self, previous_transition):
        """You probably don't want to override this method."""

        if self.on_entry(ReadOnlyStateWrapper(previous_transition)) is False:
            # abort if the on_entry is False
            return Transition(
                origin=self.__class__,
                target=END,
            )
        else:
            next_state_transition = self.do_body(previous_transition)
            if next_state_transition is None:
                next_state_transition = Transition(
                    origin=self.__class__,
                    target=END,
                )

            if next_state_transition.origin is None:
                next_state_transition.origin = self.__class__

            # on_exit can override the next_state for whatever reason (error
            # transitioning, for example)
            next_state_transition = self.on_exit(
                ReadOnlyStateWrapper(next_state_transition)
            ) or next_state_transition

            return next_state_transition
