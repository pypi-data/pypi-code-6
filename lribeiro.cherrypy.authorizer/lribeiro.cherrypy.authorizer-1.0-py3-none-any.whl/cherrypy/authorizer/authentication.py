import cherrypy

from .utils import redirect
from ._constants import (
    AUTHENTICATOR,
    LOGIN_REDIRECT,
    LOGOUT_REDIRECT,
    USER_SESSION_KEY,
)


class Identity:
    def __init__(self, id_, display: str=None, data=None):
        self.id = id_
        self.display = display
        self.data = data


class AuthenticationError(Exception):
    pass


def is_authenticated() -> bool:
    if not USER_SESSION_KEY in cherrypy.session:
        return False

    current_user = cherrypy.session[USER_SESSION_KEY]

    if not isinstance(current_user, Identity):
        raise Exception('Wrong identity model')

    return True


def authenticate(**credentials) -> Identity:
    authenticator = cherrypy.request.config.get(AUTHENTICATOR, None)

    if not authenticator:
        raise Exception('Cannot authenticate without an auth function')

    user = authenticator(**credentials)

    if not isinstance(user, Identity):
        raise Exception('Authenticator function must return \'Identity\' object')

    if not user:
        raise AuthenticationError()

    cherrypy.session[USER_SESSION_KEY] = user
    return user


class AuthControllerDefaultDispatcher:
    @cherrypy.expose
    def login(self, _next=None, **credentials):
        if cherrypy.request.method != 'POST':
            raise cherrypy.NotFound()

        authenticate(**credentials)
        redirect(_next, LOGIN_REDIRECT)

    @cherrypy.expose
    def logout(self, _next=None):
        if cherrypy.request.method != 'POST':
            raise cherrypy.NotFound()

        del cherrypy.session[USER_SESSION_KEY]
        cherrypy.lib.sessions.expire()

        redirect(_next, LOGOUT_REDIRECT)


class _Login:
    exposed = True
    POST = AuthControllerDefaultDispatcher.login


class _Logout:
    exposed = True
    POST = AuthControllerDefaultDispatcher.logout


class AuthControllerMethodDispatcher:
    exposed = True
    login = _Login()
    logout = _Logout()