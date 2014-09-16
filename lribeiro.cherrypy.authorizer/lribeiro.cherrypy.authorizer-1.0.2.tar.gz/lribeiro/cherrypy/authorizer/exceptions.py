class AuthenticationError(Exception):
    pass


class MissingAuthenticatorError(Exception):
    def __init__(self):
        super(MissingAuthenticatorError, self).__init__('Cannot authenticate without an authentication function')


class WrongIdentityClassError(Exception):
    def __init__(self):
        msg = 'User identity must be an instance or subclass of "lribeiro.cherrypy.authorizer.authentication.Identity"'
        super(WrongIdentityClassError, self).__init__(msg)