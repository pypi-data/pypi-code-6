from pyramid.config import Configurator
from smallsettings import Factory

from .unpackrequest import UnpackRequest
from .command import CommandsApplication
from .errors import PluginNotFound


class Application(object):

    """Prepering and configuring project."""

    def __init__(self, module, make_routes):
        self.make_routes = make_routes
        self.module = module
        self.initialize_unpacker()
        self.plugins = []
        self.plugin_types = []
        self.controller_plugins = []
        self.commands = None

    def initialize_unpacker(self):
        self.unpacker = UnpackRequest()
        self.unpacker.add('POST', lambda req: req.POST)
        self.unpacker.add('GET', lambda req: req.GET)
        self.unpacker.add('matchdict', lambda req: req.matchdict)
        self.unpacker.add('settings', lambda req: req.registry['settings'])
        self.unpacker.add('registry', lambda req: req.registry)
        self.unpacker.add('route', lambda req: req.route_path)

    def add_plugin(self, plugin):
        if type(plugin) in self.plugin_types:
            # add plugin only once
            # TODO: this should raise an error
            return
        plugin.init(self)
        plugin.add_unpackers(self.unpacker)
        plugin.add_controller_plugins(self.controller_plugins)
        self.plugin_types.append(type(plugin))
        self.plugins.append(plugin)

    def __call__(self, settings={}):
        self.settings = self.generate_settings(settings)
        self.make_before_config()
        self.create_config()
        self.make_after_config()
        self.make_pyramid_includes()
        self.make_routes(self)
        self.make_registry(self.config.registry)

        return self.config.make_wsgi_app()

    def run_commands(self, settings={}):
        self.settings = self.generate_settings(settings)
        self.commands = CommandsApplication(self)
        self.commands()

    def generate_settings(self, settings):
        self._settings, self._paths = self.get_settings(self.module, settings)
        merged = self._settings.merged(self._paths)
        return merged.to_dict()

    @classmethod
    def get_settings(cls, module, settings={}, additional_modules=None):
        additional_modules = additional_modules or [
            ('local', False),
        ]
        factory = Factory('%s.application' % (module))
        settings, paths = factory.make_settings(
            settings=settings,
            additional_modules=additional_modules,)
        return settings, paths

    @classmethod
    def get_settings_for_tests(cls, module, settings={}):
        additional_modules = [
            ('local', False),
            ('tests', True),
            ('local_test', False),
        ]

        return cls.get_settings(module, settings, additional_modules)

    def create_config(self):
        self.config = Configurator(
            settings=self.settings,
        )

    def make_before_config(self):
        for plugin in self.plugins:
            plugin.before_config()

    def make_after_config(self):
        for plugin in self.plugins:
            plugin.add_request_plugins()
        for plugin in self.plugins:
            plugin.after_config()

    def make_pyramid_includes(self):
        for plugin in self.plugins:
            plugin.make_config_include_if_able()
        self.config.commit()

    def make_registry(self, registry):
        registry['unpacker'] = self.unpacker
        registry['settings'] = self.settings
        registry['controller_plugins'] = self.controller_plugins
        for plugin in self.plugins:
            plugin.add_to_registry()

    def add_controller_plugin(self, plugin):
        self.controller_plugins.append(plugin)

    def _validate_dependency_plugin(self, plugin):
        if not plugin in self.plugin_types:
            raise PluginNotFound(plugin)
