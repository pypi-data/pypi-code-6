class Plugin(object):

    @property
    def config(self):
        return self.app.config

    @property
    def registry(self):
        return self.config.registry

    @property
    def settings(self):
        return self.app.settings

    def init(self, app):
        self.app = app

    def make_config_include_if_able(self):
        try:
            self.config.include(self.get_include_name())
        except NotImplementedError:
            pass

    def get_include_name(self):
        raise NotImplementedError()

    def add_to_registry(self):
        pass

    def before_config(self):
        pass

    def after_config(self):
        pass

    def add_unpackers(self, unpacker):
        pass

    def add_controller_plugins(self, plugins):
        pass
