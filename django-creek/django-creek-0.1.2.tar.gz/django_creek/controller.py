from django.conf.urls import url
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.conf import settings


class Completed(object):
    def __init__(self, session, namespace):
        self.session = session
        self.key = namespace + '_completed'

    def get(self):
        try:
            return self.session[self.key]
        except KeyError: # Session hasn't been made yet
            self.session[self.key] = []
            return self.session[self.key]

    def complete(self, state_name):
        completed = self.get()

        if state_name not in completed:
            self.session[self.key].append(state_name)
            self.session.modified = True


class Debug(object):
    def __init__(self, request, namespace):
        self.session = request.session
        self.key = namespace + '_debug'

        if request.GET.get('flow_debug'):
            self.set(request.GET['flow_debug'])

    def get(self):
        if not settings.DEBUG:
            return False
        try:
            return self.session[self.key] == 'true'
        except KeyError: # Session hasn't been made yet
            return False

    def set(self, debug):
        self.session[self.key] = debug


class FlowController(object):

    @property
    def flow(self):
        raise ImproperlyConfigured('"flow" on FlowController not defined.')

    @property
    def _flow(self):
        _flow = {}
        for i, state in enumerate(self.flow):
            try:
                _flow[state] = [self.flow[i + 1]]
            except IndexError:
                _flow[state] = []
        return _flow

    @property
    def _state_names(self):
        return [state.state for state in self._flow]

    def dispatch(self, request, state_name=None):
        namespace = self.__class__.__name__

        debug = Debug(request, namespace)
        self.completed = Completed(request.session, namespace)

        self.initial_state = self.flow[0] # Initial state

        if debug.get() or self._is_allowed(state_name):
            return self._get_state(state_name).as_view(controller=self)(request)
        else:
            return redirect(self._get_last_completed())

    @classmethod
    def urlpatterns(cls):
        urls = []
        for state in cls.flow:
            name = state.state
            reg = r'%s/$' % name
            pattern = url(reg, cls().dispatch, {'state_name': name}, name=name)
            urls.append(pattern)
        return urls

    def complete(self, state_name):
        self.completed.complete(state_name)

    def next(self, state_name, next_name=None):
        self.complete(state_name)
        state = self._get_state(state_name)

        try:
            next_state = self._flow[state][0]
        except IndexError: # No next state. Use the last one.
            next_state = self.flow[-1]

        return redirect(next_state.state)

    def _is_allowed(self, state_name):
        state = self._get_state(state_name)

        # First state is always allowed
        if state == self.initial_state:
            return True

        completed = self.completed.get()

        # If we've already completed this, go ahead
        if state_name in completed:
            return True

        # If we've completed the state before, make it happen
        for prereq, allowed in self._flow.items():
            if prereq.state in completed and state in allowed:
                return True

        return False

    def _get_last_completed(self):
        try:
            return self.completed.get()[-1]
        except IndexError:
            # Nothing completed, return initial state
            return self.initial_state.state

    def _get_state(self, state_name):
        for state in self.flow:
            if state.state == state_name:
                return state
        raise ImproperlyConfigured('No FlowState "%s" found' % state_name)

