import sys
from flask import make_response, redirect, request, current_app
from werkzeug.local import LocalProxy
from session import Session
from functools import wraps

class Dissect():

    def __init__(self, app=None, config={}):
        self.app = app
        if app is not None:
            self.init_app(app)

        self.config = config
        self.callbacks = {}
        self.session = LocalProxy(self.get_session)

        def _redirect():
            url = self.config.get('authentication_url')
            return redirect(url, code=401)

        msg = self.config.get('unauthorized_message')
        if not msg:
            msg = "Unauthorized"

        def _unauthorized():
            return make_response(msg, 401)

        if self.config.get('authentication_url'):
            self.unauthorized = _redirect
        else:
            self.unauthorized = _unauthorized

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

            @wraps(fun)
            def w2(*args, **kwargs):
                return fun(*args, **kwargs)
            return w2
        return w

#============================================================================================================
    def __call__(self, name):
        def w(fun):
            @wraps(fun)
            def w2(*args, **kwargs):

                valfun = self.callbacks.get(name)

                if not valfun:
                    sys.stderr.write('Invalid callback function: %s\n' % name)
                    return self.unauthorized()

                session = self.get_session()

                r = valfun(session=session)

                if not r:
                    return self.unauthorized()
                return fun(*args, **kwargs)
            return w2
        return w

#============================================================================================================
