import sys
import time
from flask import _app_ctx_stack as stack, make_response, request, current_app
from werkzeug.local import LocalProxy
from session import Session

class Dissect():

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

        self.time = None
        self.config = {}
        self.callbacks = {}
        self.session = LocalProxy(self.get_session)

#============================================================================================================
    def init_app(self, app):
    
        @self.app.before_request
        def request_enter():
            current_app._session = Session(request.cookies)

        @self.app.after_request
        def request_exit(response):
            session = self.get_session()
            return session.set_cookie(response)
#============================================================================================================
    def get_session(self):
        return current_app._session
#============================================================================================================
    def register(self, name):

        def w(fun):

            self.callbacks[name] = fun

            def w2():
                return fun

            return w2
        return w

#============================================================================================================
    def __call__(self, name):
        def w(fun):
            def w2(*args, **kwargs):

                valfun = self.callbacks.get(name)

                if not valfun:
                    sys.stderr.write('Invalid callback function: %s\n' % name)
                    return make_response('Falhou', 401)

                session = self.get_session()

                r = valfun(session=session)

                if not r:
                    return make_response('Falhou', 401)
                return fun(*args, **kwargs)
            return w2
        return w

#============================================================================================================
