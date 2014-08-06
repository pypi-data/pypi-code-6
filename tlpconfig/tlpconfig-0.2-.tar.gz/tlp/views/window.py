from . import Status, CategoriesGroup, load_view 
from gi.repository import Gtk


class Window():
    UI = ('window.ui', 'header.ui')

    def __init__(self, loader):
        loader.connect(self)
        self._load_childs(loader)

    def load_configuration(self, configuration):
        self.config = configuration
        self.header.set_subtitle(configuration.file_path)
    
        self.categories = CategoriesGroup(self.categories_list, self.stack)
        self.categories.render(configuration.load())

    def save(self, button):
        parameters = self.categories.get_parameters()
        self.config.save(parameters)

    def save_as(self, button):
        buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                   Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        dialog = Gtk.FileChooserDialog('Save TLP configuration file',
                                       self.window, Gtk.FileChooserAction.SAVE,
                                       buttons)

        if dialog.run() == Gtk.ResponseType.OK:
            parameters = self.categories.get_parameters()
            self.config.save_as(parameters, dialog.get_filename())
            self.header.set_subtitle(self.config.file_path)
    
        dialog.destroy()

    def status(self, button):
        load_view(Status).show(self.window)

    def show(self):
        self.window.present()

    def select_row(self, listbox, row):
        if row:
            self.stack.set_visible_child_name(Gtk.Buildable.get_name(row))

    def _load_childs(self, loader):
        self.panel = loader.get('panel')
        self.window = loader.get('window')
        self.categories_list = loader.get('categories')

        self.stack = self._create_categories_stack()
        loader.get('category_content').add(self.stack)

        self.header = loader.get('header')
        self.window.set_titlebar(self.header)

    def _create_categories_stack(self):
        stack = Gtk.Stack()
        stack.set_homogeneous(False)
        stack.set_visible(True)
        return stack
