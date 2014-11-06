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
from solid.transition import Transition, START


def is_entry_state(state_class):
    """marks a state as a valid initial state for a machine, which means the
    following changes are made:
        1. the run() method is patched to not need as incoming_transition
        2. a __call__ method is applied to the state so it can be used like a
           function.
    """
    state_class.IS_ENTRY_STATE = True

    def new_call(self, **body_args):
        starting_transition = Transition(
            origin=START,
            target=state_class,
            **body_args
        )
        return self.run(starting_transition)
    state_class.__call__ = new_call

    return state_class
