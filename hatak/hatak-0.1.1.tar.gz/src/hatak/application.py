from pyramid.config import Configurator
from smallsettings import Factory

from .plugins import Jinja2Plugin, SqlPlugin, BeakerPlugin, DebugtoolbarPlugin
from .plugins import LoggingPlugin
from .unpackrequest import UnpackRequest


class Application(object):

    """Prepering and configuring project."""

    def __init__(self, module, make_routes):
        self.make_routes = make_routes
        self.module = module
        self.initialize_unpacker()
        self.plugins = []
        self.controller_plugins = []
        self.generate_plugins()

    def initialize_unpacker(self):
        self.unpacker = UnpackRequest()
        self.unpacker.add('POST', lambda req: req.POST)
        self.unpacker.add('GET', lambda req: req.GET)
        self.unpacker.add('matchdict', lambda req: req.matchdict)
        self.unpacker.add('settings', lambda req: req.registry['settings'])
        self.unpacker.add('session', lambda req: req.session)
        self.unpacker.add('registry', lambda req: req.registry)

    def generate_plugins(self):
        self.add_plugin(LoggingPlugin())
        self.add_plugin(Jinja2Plugin())
        self.add_plugin(SqlPlugin())
        self.add_plugin(BeakerPlugin())
        self.add_plugin(DebugtoolbarPlugin())

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
        plugin.init(self)
        plugin.add_unpackers(self.unpacker)
        plugin.add_controller_plugins(self.controller_plugins)

    def __call__(self, settings={}):
        self.settings = self.generate_settings(settings)
        self.make_before_config()
        self.create_config()
        self.make_after_config()
        self.make_pyramid_includes()
        self.make_routes(self)
        self.make_registry()

        return self.config.make_wsgi_app()

    def generate_settings(self, settings):
        self._settings, self._paths = self.get_settings(self.module, settings)
        merged = self._settings.merged(self._paths)
        return merged.to_dict()

    @classmethod
    def get_settings(cls, module, settings={}):
        factory = Factory('%s.application' % (module))
        settings, paths = factory.make_settings(
            settings=settings,
            additional_modules=[
                ('local', False),
            ])
        return settings, paths

    def create_config(self):
        self.config = Configurator(
            settings=self.settings,
        )

    def make_before_config(self):
        for plugin in self.plugins:
            plugin.before_config()

    def make_after_config(self):
        for plugin in self.plugins:
            plugin.after_config()

    def make_pyramid_includes(self):
        for plugin in self.plugins:
            plugin.make_config_include_if_able()
        self.config.commit()

    def make_registry(self):
        self.config.registry['unpacker'] = self.unpacker
        self.config.registry['settings'] = self.settings
        self.config.registry['controller_plugins'] = self.controller_plugins
        for plugin in self.plugins:
            plugin.add_to_registry()

    def add_controller_plugin(self, plugin):
        self.controller_plugins.append(plugin)
