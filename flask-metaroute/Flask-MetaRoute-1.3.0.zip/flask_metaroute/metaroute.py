from flask_metaroute.func import attach_controllers
import importlib


class MetaRoute:

    def __init__(self, app = None, ctrl_pkg = None):
        """**DEPRECATED**

        Use MetaRoute.Apply instead
        """
        if app:
            self.app = app
            self.init_app(self.app, ctrl_pkg)

    @staticmethod
    def init_app(app, ctrl_pkg = None):
        """**DEPRECATED**

        Use MetaRoute.Apply instead
        """
        pkg = ctrl_pkg or app.config['METAROUTE_CONTROLLERS_PKG']
        if isinstance(pkg, str):
            pkg = importlib.import_module(pkg)

        attach_controllers(app, pkg)

    @staticmethod
    def Apply(app, ctrl_pkg=None):
        pkg = ctrl_pkg or app.config['METAROUTE_CONTROLLERS_PKG']
        if isinstance(pkg, str):
            pkg = importlib.import_module(pkg)

        attach_controllers(app, pkg)
        return app