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
from solid.states.base_state import BaseState
from solid.transition import to


class SingleTargetState(BaseState):
    """Shorthand state that will automatically transition to the state
    registered through SingleTargetState.next_state --- just have bod() return
    a dictionary, and SingleTargetState will take care of constructing a
    Transition for you:

        class MyMachine(BaseMachine):
            class LazyState(SingleTargetState):
                def body():
                    #...
                    return {
                        'your': keys,
                        'go': here,
                    }

            @LazyState.next_state
            class StudiousState(BaseState):
                def body(your, go):
                    ...
    """


    @classmethod
    def next_state(cls, state_class):
        cls.target = state_class
        return state_class

    def do_body(self, previous_transition):
        results = self.body(**previous_transition.kwargs)

        return to(self.target, **results)
