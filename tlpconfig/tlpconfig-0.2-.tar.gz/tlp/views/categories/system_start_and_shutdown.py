from gi.repository import Gtk
from .category import Category
from itertools import chain


class SystemStartAndShutdown(Category):
    CATEGORY='SYSTEM_START_AND_SHUTDOWN'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)
        self.set_groups(configuration_groups)
    
    def load_controls(self):
        super().load_controls()
        self.startup_actions = self.load('actions_on_startup')

    def get_groups(self):
        for param, ui in self.parameters.values():
            if isinstance(ui, Gtk.Switch):
                param.value = ui.get_active()
            else:
                param.value = ' '.join([children.get_active() 
                                        for children in ui.get.children()])

    def change_restore_devices_on_startup(self, switch, gparam):
        self.startup_actions.set_sensitive(not switch.get_active())

    def change_restore_devices_on_startup(self, switch, gparam):
        self.startup_actions.set_visible(not switch.get_active())
