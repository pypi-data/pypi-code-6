from . import create_category_loader
from .categories import *
from gi.repository import Gtk

class CategoriesGroup:
    def __init__(self, list_control, stack):
        self.list_control = list_control
        self.stack = stack

    def render(self, categories):
        load = create_category_loader(categories)
        self.categories = [load(FileSystem), 
                           load(ProcessorAndFrequenceScaling),
                           load(Kernel),
                           load(Undervolting),
                           #load(DisksAndControllers),
                           load(PciExpressBus),
                           load(GraphicsCards),
                           load(Networking),
                           load(Audio),
                           #load(DriveSlotUltrabay),
                           #load(RuntimePowerManagement),
                           #load(Usb),
                           load(SystemStartAndShutdown),
                           load(WirelessRadioSwitch),
                           load(BatteryChargeThresholds)]

        self._render_all()

    def _render_all(self):
        def header(row, before, user_data):
            if before and not row.get_header():
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                row.set_header(sep)

        self.list_control.set_header_func(header, None)

        for category in self.categories:
            self.list_control.add(category.menu)
            self.stack.add_named(category.panel,
                                 Gtk.Buildable.get_name(category.menu))
    
    def get_parameters(self):
        return [parameter 
                for view in self.categories 
                for parameter in view.get_parameters()]
