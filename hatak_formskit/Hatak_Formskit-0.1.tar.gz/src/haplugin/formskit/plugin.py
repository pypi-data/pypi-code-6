from hatak.plugin import Plugin
from hatak.controller import ControllerPlugin
from haplugin.jinja2 import Jinja2Plugin

from .helpers import FormWidget


class FormPlugin(Plugin):

    def __init__(self, widget=FormWidget):
        self.widget = widget

    def add_controller_plugins(self, plugins):
        FormControllerPlugin.widget = self.widget
        plugins.append(FormControllerPlugin)

    def validate_plugin(self):
        self.app._validate_dependency_plugin(Jinja2Plugin)


class FormControllerPlugin(ControllerPlugin):

    def add_controller_methods(self):
        self.add_method('add_form')

    def add_form(self, formcls, name='form', *args, **kwargs):
        form = formcls(self.request, *args, **kwargs)
        self.controller.add_helper(name, self.widget, form)
        return form
