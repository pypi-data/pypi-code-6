from flask import Flask

from highfield import loading
from highfield.defaults import *
from config import *

class Application(Flask):

    def __init__(self):
        template_folder = loading.path('views')
        static_folder = loading.path('static')
        super(Application, self).__init__(__name__,
                                          template_folder=template_folder,
                                          static_folder=static_folder)
        self.configure()
        self.session_cookie_name = session_cookie_name
        self.secret_key = session_secret_key
        self.csrf_token_lifespan = csrf_token_lifespan
        pass

    def configure(self):
        self.controllers = loading.namespace('controllers')
        self.models = loading.namespace('models')

        for path, route in routes:
            c_name, a_name = route.get('to').split('.')
            methods = [m.upper() for m in route.get('via')]

            def closure(c_name, a_name):
                def dispatch(*args, **kwargs):
                    controller = getattr(self.controllers, c_name)(self, a_name)
                    return getattr(controller, a_name).__call__(*args, **kwargs)
                return dispatch
            self.add_url_rule(path, route.get('to'), closure(c_name, a_name), methods=methods)
            pass
        return self

    def run(self, network=False, **kwargs):
        if network:
            kwargs.update(host='0.0.0.0')
            pass
        super(Application, self).run(**kwargs)
        pass
    pass

