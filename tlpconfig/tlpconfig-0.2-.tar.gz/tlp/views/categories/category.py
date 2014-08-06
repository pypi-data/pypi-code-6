from gi.repository import Gtk
from itertools import chain
from ...models import (TextParameter, BooleanParameter,
                       ListParameter, NumericParameter)
from ..binders import ParameterBinderSelector


class Category:
    def __init__(self, category, loader):
        loader.connect(self)
        self.loader = loader
        self.load_controls()

        self.value_binders = ParameterBinderSelector()
    
    def load_controls(self):
        self.menu = self.loader.get('_'.join([self.CATEGORY.lower(), 'row']))
        self.panel = self.loader.get('_'.join([self.CATEGORY.lower(), 'panel']))

    def load(self, control_id):
        return self.loader.get(control_id)
    
    def _active_switch_changed(self, switch, parameter):
        group_name = Gtk.Buildable.get_name(switch).replace('ACTIVE_', '')

        group = [group for group in self.groups if group.name == group_name][0]
        group.is_active = switch.get_active()

        self.load(group_name).set_sensitive(switch.get_active())

    def _set_enabled_groups(self):
        for group in self.groups:
            switch = self.load('ACTIVE_' + group.name)
            switch.set_active(group.is_active)
            self._active_switch_changed(switch, None)

    def set_groups(self, groups):
        self.groups = groups
        self._set_enabled_groups()

        parameters = chain.from_iterable(group.parameters.values()
                                         for group in self.groups)

        for parameter in parameters:
            self.value_binders  \
                .get_from(parameter) \
                .set_value_to(self.load(parameter.name))

    def get_parameters(self):
        parameters = list(chain.from_iterable(group.parameters.values()
                                         for group in self.groups))

        for parameter in parameters:
            parameter.value = self.value_binders  \
                                  .get_from(parameter) \
                                  .get_value_from(self.load(parameter.name))

        return parameters
