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

from solid.machines.base_machine import BaseMachine
from solid.transition import END


class SteppedMachine(BaseMachine):

    def start(self, **kwargs):
        """Only enter the first state of the machine and add it to the
        history; afterwards, use the step() function to progress."""
        next_transition = self._entry_state(**kwargs)
        self._history.append(next_transition)

    def step(self):
        """Follow the last returned transition."""
        previous = self._history[-1]

        if previous.target is END:
            return self._return_value

        next_transition = self._initialized_states[previous.target].run(
            previous_transition=previous,
        )
        self._history.append(next_transition)
