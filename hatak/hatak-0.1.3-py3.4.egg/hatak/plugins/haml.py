from .plugin import Plugin
from hatak.plugins.jinja2 import Jinja2HelperMany


class HamlPlugin(Plugin):

    def before_config(self):
        extensions = self.settings.get('jinja2.extensions', [])
        extensions.append('hamlish_jinja.HamlishExtension')
        self.settings['jinja2.extensions'] = extensions

    def add_to_registry(self):
        self.config.add_jinja2_renderer('.haml')


class HamlHelperMany(Jinja2HelperMany):

    def get_template(self, name, prefix=None):
        prefix = prefix or self.prefix
        return '%s/%s.haml' % (prefix, name)
