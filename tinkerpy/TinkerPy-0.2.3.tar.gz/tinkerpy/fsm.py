'''\

:mod:`tinkerpy.fsm` -- A Finite State Machine API
-------------------------------------------------

This module implements an API for defining and executing finite state machines
(FSMs) defined as classes. A FSM is a mathematical model consisting of
,,states'' and a set of ,,transitions'' between or on them. A FSM instance is
always in only one of those states. If a transitions between two states is
executed, after execution the new state of the instance is the target state of
the transition.


Defining a FSM
^^^^^^^^^^^^^^
A finite state machine is a sub-class of the following class:

.. autoclass:: FiniteStateMachine

On sub-classes states and transitions should be defined, these can be associated
with arbitrary data. Each state and transition has a name, the name of a
transition identifies it under its source state. Additionally methods of the
class can be specified to be called on executing a transition or on leaving or
entering a state. States must not be defined specially, they can also be given
indirectly by referencing them in transitions.

The following functions can be executed in the body of a FSM class to define
states or transitions, respectively:

.. autofunction:: state_data
.. autofunction:: transition

Executing one of the following functions creates a decorator to be applied to
methods in the body of a FSM class, which registers those methods by name to
be executed on entering or leaving a state or on executing a transition:

.. autofunction:: entering_state
.. autofunction:: leaving_state
.. autofunction:: on_transition


An Example FSM
^^^^^^^^^^^^^^

>>> class MyFSM(FiniteStateMachine):
...    FSM_start = 'juvenile'
...
...    @entering_state()
...    def juvenile(self, obj):
...        print('Born again.')
...        return 'new body'
...
...    @entering_state()
...    def adult(self, obj):
...        print('Now being adult.')
...        return 'new responsibilities'
...
...    @leaving_state('adult')
...    def leave_adult(self, obj):
...        print('Getting old.')
...
...    @on_transition('juvenile', 'adult')
...    def grow_up(self, obj):
...        print('Growing up.')
...        return 'changed body'
...
...    @on_transition('adult', 'dead')
...    def die(self, obj):
...        print('Dying.')
...
...    transition('reincarnate', 'dead', 'juvenile')
...

>>> class MyObject(object): pass

>>> my_fsm = MyFSM()
>>> obj = MyObject()
>>> print(my_fsm(obj).name) # retrieve name of current state
juvenile

>>> my_fsm(obj, 'grow_up')
Growing up.
Now being adult.
('changed body', 'new responsibilities')
>>> print(my_fsm(obj).name)
adult

>>> my_fsm(obj, 'die')
Getting old.
Dying.
>>> print(my_fsm(obj).name)
dead

>>> my_fsm(obj, 'reincarnate')
Born again.
'new body'
>>> print(my_fsm(obj).name)
juvenile

'''
import abc
import collections

from tinkerpy import metaclass

def _get_state(machine_dict, name):
    try:
        states = machine_dict['_FSM_states']
    except KeyError:
        states = {}
        machine_dict['_FSM_states'] = states
    try:
        return states[name]
    except KeyError:
        state = State(name)
        states[name] = state
    return state


def state_data(state_name, **data):
    '''\
    Associates the given data with a state. The data dictionary of the state
    with the given ``state_name`` is updated with ``data``.

    :param state_name: The name of the state.
    :param data: The entries to update the state's data dictionary with.
    '''
    import inspect
    stack = inspect.stack()
    frame = stack[1][0]
    caller_locals = frame.f_locals
    del stack, frame
    state = _get_state(caller_locals, state_name)
    state._data.update(data)


def _on_state(state_name, direction):
    state_attribute_name = '_{}_method_name'.format(direction)
    def decorator(func):
        import inspect
        stack = inspect.stack()
        frame = stack[1][0]
        caller_locals = frame.f_locals
        del stack, frame
        state = _get_state(caller_locals,
            func.__name__ if state_name is None else state_name)
        setattr(state, state_attribute_name, func.__name__)
        return func
    return decorator


def entering_state(state_name=None):
    '''\
    The result of this function should be used as a method decorator to register
    the decorated function which will be executed on entering a state. If no
    state is given the name of the decorated method denotes the state.

    :param state_name: The name of the state the decorated method should be
        executed on entering. If this is :const:`None` the name of the decorated
        method denotes the state.
    :returns: A method decorator.
    '''
    return _on_state(state_name, 'entering')


def leaving_state(state_name=None):
    '''\
    The result of this function should be used as a method decorator to register
    the decorated function which will be executed on leaving a state. If no
    state is given the name of the decorated method denotes the state.

    :param state_name: The name of the state the decorated method should be
        executed on leaving. If this is :const:`None` the name of the decorated
        method denotes the state.
    :returns: A method decorator.
    '''
    return _on_state(state_name, 'leaving')


def _create_transition(machine_dict, name, data, source_name, target_name):
    source = _get_state(machine_dict, source_name)
    target = _get_state(machine_dict, target_name)
    if name in source:
        raise ValueError(
            'There already is a transition "{}" defined on state "{}".'.format(
                name, source.name))
    transition = Transition(name, data, source, target)
    source._transitions[name] = transition
    return transition


def transition(transition_name, source_name, target_name, **data):
    '''\
    Defines a transition and optionally updates the transitions's data
    dictionary.

    :param transition_name: The name of the transition to identify it under
        its source state.
    :param source_name: The name of the source state.
    :param target_name: The target state's name.
    :param data: The entries to update the transition's data dictionary with.
    '''
    transition_name = str(transition_name)
    source_name = str(source_name)
    target_name = str(target_name)
    import inspect
    stack = inspect.stack()
    frame = stack[1][0]
    caller_locals = frame.f_locals
    del stack, frame
    _create_transition(caller_locals, transition_name, data, source_name,
        target_name)


def on_transition(*args, **data):
    '''\
    The result of this function should be used as a method decorator to register
    the decorated function which will be called on executing a transition and to
    optionally update the transition's data dictionary. If no transition name is
    given the name of the decorated method denotes the transition's name.

    :param args: The positional arguments denote the transition. If there are
        three arguments, they are interpreted as transition name, source state
        name and target state name. If there are only two arguments, they are
        the source and target name while the transition name is determined by
        the decorated method's name .
    :param data: The entries to update the transition's data dictionary with.
    :returns: A method decorator.
    :raises ValueError: If there are less than 2 or more than 3 positional
        arguments.
    '''
    if len(args) < 2 or len(args) > 3:
        raise ValueError('Arguments: [transition_name,] source_name, target_name, **data')
    def register(method_name, transition_name, source_name, target_name):
        import inspect
        stack = inspect.stack()
        frame = stack[2][0]
        caller_locals = frame.f_locals
        del stack, frame
        transition_name = str(transition_name)
        source_name = str(source_name)
        target_name = str(target_name)
        transition = _create_transition(caller_locals, transition_name, data,
            source_name, target_name)
        transition._method_name = method_name
    def decorator(func):
        method_name = func.__name__
        if len(args) == 2:
            register(method_name, method_name, *args)
        else:
            register(method_name, *args)
        return func
    return decorator


@metaclass(abc.ABCMeta)
class FiniteStateMachine(collections.Mapping):
    '''\
    This abstract base class implements the finite state machine execution
    model. Subclasses represent finite state machines.

    On instanciation the metadata created by the state and transition
    definitions (done by :func:`state_data`, :func:`entering_state`,
    :func:`leaving_state`, :func:`transition` and :func:`on_transition`) is
    processed (thus the :meth:`__init__` method should always be called). Be
    aware that the bindings created by those definitions are by name of the
    methods.

    Instances allow access to the machine structure (states, transitions).
    Additionally they can be called with an object and a transition name to
    execute the transition on the object, which calls the source state's leaving
    callback, the transitions callback and the target state's entering callback
    (assuming those exist) and finally sets the attribute ``FSM_current_state``
    on the object to the target state's name.

    :raises ValueError: If there are errors in the machine's definition.
    '''
    def __init__(self):
        try:
            start_state_name = str(self.FSM_start)
        except AttributeError:
            raise ValueError(
                'This FSM does not define a start state (in attribute "FSM_start").')
        states = {}
        for machine_cls in reversed(self.__class__.mro()):
            try:
                machine_states = self._FSM_states
            except AttributeError:
                pass
            else:
                states.update(machine_states)
        if len(states) == 0:
            raise ValueError('No states are defined on this FSM.')
        try:
            start_state = states[start_state_name]
        except KeyError:
            raise ValueError('The start state "{}" is not defined on this FSM.'.format(
                start_state_name))
        self._start_state = start_state
        self._states = states

    @property
    def start_state(self):
        '''\
        The start state name.
        '''
        return self._start_state

    def __getitem__(self, state_name):
        return self._states[state_name]

    def __iter__(self):
        return iter(self._states)

    def __len__(self):
        return len(self._states)

    def __call__(self, obj, *args, **kargs):
        try:
            current_state_name = obj.FSM_current_state
        except AttributeError:
            current_state = self._start_state
        else:
            try:
                current_state = self._states[current_state_name]
            except KeyError:
                current_state = self._start_state
        if len(args) == 0:
            return current_state
        transition_name = args[0]
        args = args[1:]
        try:
            transition = current_state[transition_name]
        except KeyError:
            raise ValueError(
                'Unknown transition "{}" on state "{}".'.format(
                    transition_name, current_state.name))
        target = transition.target
        results = []
        def handle_result(result):
            if result is not None:
                results.append(result)
        handle_result(current_state._execute_leaving(self, obj, args,
            kargs))
        handle_result(transition._execute(self, obj, args, kargs))
        handle_result(target._execute_entering(self, obj, args, kargs))
        obj.FSM_current_state = target.name
        if len(results) > 1:
            return tuple(results)
        elif len(results) == 1:
            return results[0]


class _FSMObject(object):
    __slots__ = {'_name', '_data'}

    def __init__(self, name, data):
        self._name = name
        self._data = data

    @property
    def name(self):
        return self._name

    def get_data(self, name):
        return self._data[name]


class State(_FSMObject, collections.Mapping):
    __slots__ = {'_transitions', '_entering_method_name',
        '_leaving_method_name'}

    def __init__(self, name):
        _FSMObject.__init__(self, name, {})
        self._transitions = {}
        self._entering_method_name = None
        self._leaving_method_name = None

    @property
    def entering_method_name(self):
        return self._entering_method_name

    @property
    def leaving_method_name(self):
        return self._leaving_method_name

    def __getitem__(self, transition_name):
        return self._transitions[transition_name]

    def __iter__(self):
        return iter(self._transitions)

    def __len__(self):
        return len(self._transitions)

    def _execute(self, direction, machine, obj, args, kargs):
        meth_name = getattr(self, '_{}_method_name'.format(direction))
        if meth_name is None:
            return
        try:
            meth = getattr(machine, meth_name)
        except AttributeError:
            raise RuntimeError(
                'Could not find the method "{}" on FSM "{}" {} state "{}".'.format(
                    meth_name, machine, direction, self.name))
        return meth(obj, *args, **kargs)

    def _execute_leaving(self, machine, obj, args, kargs):
        return self._execute('leaving', machine, obj, args, kargs)

    def _execute_entering(self, machine, obj, args, kargs):
        return self._execute('entering', machine, obj, args, kargs)


class Transition(_FSMObject):
    __slots__ = {'_source', '_target', '_method_name'}

    def __init__(self, name, data, source, target):
        _FSMObject.__init__(self, name, data)
        self._source = source
        self._target = target
        self._method_name = None

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def method_name(self):
        return self._method_name

    def _execute(self, machine, obj, args, kargs):
        meth_name = self._method_name
        if meth_name is None:
            return
        try:
            meth = getattr(machine, meth_name)
        except AttributeError:
            raise RuntimeError(
                'Could not find the method "{}" on FSM "{}" for transition "{}" on state "{}".'.format(
                    meth_name, machine, self.name, self._source.name))
        return meth(obj, *args, **kargs)

del abc, collections, metaclass