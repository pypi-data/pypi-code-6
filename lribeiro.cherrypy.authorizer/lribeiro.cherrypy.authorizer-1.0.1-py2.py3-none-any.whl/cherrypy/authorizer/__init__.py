import cherrypy

from lribeiro.cherrypy.authorizer.authorization import authorizer_tool
from lribeiro.cherrypy.authorizer.authorization import authorize
from ._constants import AUTHENTICATOR, AUTHORIZER, LOGIN_PAGE, LOGIN_REDIRECT, LOGOUT_REDIRECT, UNAUTHORIZED_REDIRECT


# configuration dict for the namespace
_authorizer_config = dict()


# Define the configuration namespace
def _auth_namespace(k, v):
    _authorizer_config[k] = v

cherrypy.config.namespaces['auth'] = _auth_namespace

cherrypy.tools.authorizer = cherrypy.Tool('before_handler', authorizer_tool)