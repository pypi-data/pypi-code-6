from .views import Window, Shell, load_css, load_view 
from gi.repository import Gtk, Gio, Gdk
from .models import Configuration


class App(Gtk.Application):
    
    def __init__(self):
        Gtk.Application.__init__(self, application_id='TLP.Configuration')
        self.shell = load_view(Shell)
        self.window = None

    def start(self, config_file):
        self.config = Configuration(config_file)
        self.run(None)

    def do_activate(self):
        load_css('application.css', Gdk.Screen.get_default())

        if not self.window:
            self.window = load_view(Window)
            self.window.load_configuration(self.config)
            self.add_window(self.window.window)

        self.window.show()
        
    def do_startup(self):
        Gtk.Application.do_startup(self)
        
        self.set_app_menu(self.shell.menu)

        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self.shell.show_about)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new('quit', None)
        quit_action.connect('activate', lambda *args: self.quit())
        self.add_action(quit_action)
