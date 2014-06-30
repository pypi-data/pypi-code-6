from django.core.exceptions import ImproperlyConfigured

class Flow(object):
    def __init__(self, state, controller):
        self._state = state
        self._controller = controller

    def uncomplete(self):
        pass

    def complete(self):
        self._controller.complete(self._state.state)

    def next(self, next_state_name=None):
        return self._controller.next(self._state.state, next_state_name)

    def end(self):
        pass


class FlowState(object):
    controller = None

    def __init__(self, *args, **kwargs):
        controller = kwargs.get('controller')
        self.flow = Flow(self, controller)

    @property
    def state(self):
        raise ImproperlyConfigured('FlowState must have a "state" property')
