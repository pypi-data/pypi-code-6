# config keys constants
# these are available to use in your configuration
AUTHENTICATOR = 'auth.authenticator'
AUTHORIZER = 'auth.authorizer'
LOGIN_PAGE = 'auth.login_page'
LOGIN_REDIRECT = 'auth.login_redirect'
LOGOUT_REDIRECT = 'auth.logout_redirect'
UNAUTHORIZED_REDIRECT = 'auth.unauthorized_redirect'

# these are for internal use of cherrypy-authorizer
AUTH_REQUIRED = '_auth_required'
AUTH_CLAIMS = '_auth_claims'
DEFAULT_LOGIN_PAGE = '/login'
USER_SESSION_KEY = '_auth_user_session'
REQUEST_USER = 'auth_user'