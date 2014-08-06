from gi.repository import Gtk
from .. import UI_PATH

def load_view(view):
    builder = Builder()

    if isinstance(view.UI, tuple):
        for ui in view.UI:
            builder.load(UI_PATH + ui)
    else:
        builder.load(UI_PATH + view.UI)

    return view(builder)


def create_category_loader(categories):
    file_name = UI_PATH + 'categories/{0}.ui'

    def loader(view):
        builder = Builder()
        builder.load(file_name.format(view.CATEGORY.lower()))
        return view(builder, categories.get(view.CATEGORY) or [])

    return loader


def load_css(stylesheet, screen):
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(UI_PATH + stylesheet)

    context = Gtk.StyleContext()
    context.add_provider_for_screen(screen,
                                    css_provider,
                                    Gtk.STYLE_PROVIDER_PRIORITY_USER)


class Builder():
    def __init__(self):
        self.builder = Gtk.Builder()

    def load(self, file):
        self.builder.add_from_file(file)

    def connect(self, handler):
        return self.builder.connect_signals(handler)

    def get(self, object_name):
        return self.builder.get_object(object_name)
