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
        self.validate_plugin()

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

    def add_commands(self, parent):
        pass

    def validate_plugin(self):
        pass

    def add_request_plugins(self):
        pass

    def add_request_plugin(self, plugin):
        plugin = plugin()
        self.config.add_request_method(
            plugin.init,
            plugin.name,
            reify=True)


class RequestPlugin(object):

    def __init__(self, name):
        self.name = name
        self._block = False

    def init(self, request):
        self.request = request
        self.POST = request.POST
        self.GET = request.GET
        self.matchdict = request.matchdict
        self.settings = request.registry['settings']
        self.registry = request.registry
        self.route = request.route_path
        return self.return_once()

    def return_once(self):
        return self


def reify(method):
    """Decorator for making reify methods with request instance for request."""

    def requester(self, request):
        def on_request(*args, **kwargs):
            return method(self, request, *args, **kwargs)
        return on_request
    return requester
