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
from solid.states import BaseState
from solid.transition import END


class _BaseMachineMeta(type):

    STATE_CLASS = BaseState

    def __new__(cls, name, bases, attrs):
        # do the normal instantiation
        machine_class = super(_BaseMachineMeta, cls).__new__(
            cls,
            name,
            bases,
            attrs,
        )

        # add a unique State inner base class to every instance of
        # _BaseMachineMeta
        state_class = type(
            "{}State".format(name),
            (cls.STATE_CLASS,),
            {
                # State attributes
            },
        )

        states = {}
        for attr_name, attr in attrs.iteritems():
            # futz with the inheritance of states defined on the machine,
            # inserting the machine's personal state class
            if type(attr) is type and issubclass(attr, cls.STATE_CLASS):
                attr.__bases__ = (state_class,) + attr.__bases__
                states[attr_name] = attr

        # re-instantiate, with the new State classes
        attrs['_states'] = states
        machine_class = super(_BaseMachineMeta, cls).__new__(
            cls,
            name,
            bases,
            attrs,
        )
        machine_class.State = state_class
        return machine_class


class BaseMachine(object):
    """A simple state machine. Define states as inner classes
    which inherit from STATE_CLASS (default: BaseState), and
    call the start() method of an instance to get the machine
    spinning:
        class MyMachine(BaseMachine):
            @is_entry_state
            class Entry(BaseState):
                def body():
                    ...

        machine = MyMachine()
        machine.start()
    """

    __metaclass__ = _BaseMachineMeta

    def __init__(self):
        self._return_value = None
        self._initialized_states = {}
        self._history = []
        # instantiate the states for this instance of the machine
        for name, value in self._states.iteritems():
            state = value(parent_machine=self)
            if value.IS_ENTRY_STATE:
                new_name = value.get_instance_attr_name()
                self._entry_state = state
            else:
                new_name = "_{}".format(value.get_instance_attr_name())

            setattr(self, new_name, state)

            # for ease of transitioning, hit this up.
            self._initialized_states[value] = state

    def start(self, **kwargs):
        transition = self._entry_state(**kwargs)
        while transition.target is not END:
            self._history.append(transition)
            transition = self._initialized_states[transition.target].run(
                previous_transition=transition,
            )

        # add the transition to END to history as well.
        self._history.append(transition)
        return self._return_value

    def set_return_value(self, value):
        """ call this method from a terminal state to give the state machine's
        run a summary return value"""
        self._return_value = value

    @property
    def history(self):
        return list(self._history)
