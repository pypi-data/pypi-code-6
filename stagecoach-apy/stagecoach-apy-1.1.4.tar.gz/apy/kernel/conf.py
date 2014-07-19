import yaml
from os.path import realpath, dirname, isabs


class Settings:
    MERGEABLE_SUBSETTINGS = ['imports', 'routes', 'parameters', 'services']

    def __init__(self, environment, config_dir):
        self.server_adapter = 'tornado'
        self.server = {}
        self.routes = {}
        self.error_handler = 'apy.handler.DefaultErrorHandler'
        self.debug = False
        self.parameters = {}
        self.services = {}
        config_dir = config_dir.rstrip('/')

        settings = self._settings_yml_loader('%s/settings_%s.yml' % (config_dir, environment))

        settings = self._import_subsettings(settings, config_dir)

        if 'server_adapter' in settings:
            self.server_adapter = settings['server_adapter']

        if 'server' in settings:
            self.server = settings['server']

        if 'routes' in settings:
            self.routes = settings['routes']

        if 'debug' in settings:
            self.debug = settings['debug']

        if 'error_handler' in settings:
            self.error_handler = settings['error_handler']

        if 'parameters' in settings:
            self.parameters = settings['parameters']

        if 'services' in settings:
            self.services = settings['services']

    def _import_subsettings(self, settings, working_dir):
        if 'imports' in settings and len(settings['imports']) > 0:
            import_file = settings['imports'].pop()
            if not isabs(import_file):
                import_file = realpath('%s/%s' % (working_dir, import_file))
            imported_settings = self._settings_yml_loader(import_file)
            settings = self._overwrite_unmergeable_subsettings(settings, imported_settings)
            settings = self._merge_subsettings(settings, imported_settings)
            return self._import_subsettings(settings, dirname(import_file))
        else:
            return settings

    def _overwrite_unmergeable_subsettings(self, settings, imported_settings):
        for subsetting_key, subsetting_value in imported_settings.items():
            if subsetting_key not in Settings.MERGEABLE_SUBSETTINGS and subsetting_key not in settings:
                settings[subsetting_key] = subsetting_value
        return settings

    def _merge_subsettings(self, settings, imported_settings):
        for mergeable_subsetting in Settings.MERGEABLE_SUBSETTINGS:
            settings = self._merge_subsetting(settings, imported_settings, mergeable_subsetting)

        return settings

    @staticmethod
    def _merge_subsetting(settings, imported_settings, key):
        if key in imported_settings:
            if key in settings:
                if isinstance(settings[key], dict):
                    settings[key] = dict(list(imported_settings[key].items()) + list(settings[key].items()))
                if isinstance(settings[key], list):
                    settings[key] = imported_settings[key] + settings[key]
            else:
                settings[key] = imported_settings[key]

        return settings

    @staticmethod
    def _settings_yml_loader(file_path):
        """ @type file_path: str """
        settings_stream = open(file_path, "r")
        settings_generator = yaml.load_all(settings_stream)

        app_settings = {}
        for app_settings_ in settings_generator:
            for key, value in app_settings_.items():
                app_settings[key] = value

        return app_settings
