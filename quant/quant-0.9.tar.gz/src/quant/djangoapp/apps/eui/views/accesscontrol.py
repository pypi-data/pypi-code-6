from quant.djangoapp.apps.eui.views.base import QuantView
import quant.command
from dm.exceptions import KforgeCommandError
import random

class AuthenticateView(QuantView):

    def __init__(self, **kwds):
        super(AuthenticateView, self).__init__(**kwds)
        self.isAuthenticateFail = False

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Welcome', 'url': '/help/'},
        ]
        if self.session:
            self.minorNavigation.append(
                {'title': 'Log out',      'url': '/logout/'},
            )
        else:
            self.minorNavigation.append(
                {'title': 'Log in',       'url': '/login/'},
            )
            if self.canCreatePerson():
                self.minorNavigation.append(
                    {'title': 'Register',     'url': '/persons/create/'},
                )

    def canAccess(self):
        return True

    def authenticate(self):
        if self.session:
            return True
        params = self.request.POST.copy()
        name = params['name']
        password = params['password']
        command = quant.command.PersonAuthenticate(name, password)
        try:
            command.execute()
        except KforgeCommandError, inst:
            msg = "Login authentication failure for person name '%s'." % name
            self.logger.warn(msg)
        else:
            self.startSession(command.person)

    def setContext(self):
        super(AuthenticateView, self).setContext()
        self.setAuthenticationContext()
        self.context.update({
            'canCreatePerson': self.canCreatePerson(),
            'isAuthenticateFail': self.isAuthenticateFail,
        })

    def setAuthenticationContext(self):
        if self.request.POST:
            params = self.request.POST.copy()
            self.context.update({
                'name': params.get('name', ''),
                'password': params.get('password', ''),
            })


class LoginView(AuthenticateView):

    templatePath = 'login'
    minorNavigationItem = '/login/'

    def getResponse(self, returnPath=''):
        if self.request.POST:
            self.authenticate()
            params = self.request.POST.copy()
            returnPath = params.get('returnPath', '')
            if returnPath:
                if not returnPath.startswith('/'):
                    returnPath = '/' + returnPath
                self.returnPath = returnPath
            if self.session:
                if returnPath:
                    self.setRedirect(returnPath)
            else:
                self.isAuthenticateFail = True
        elif returnPath:
            self.returnPath = returnPath
        return super(LoginView, self).getResponse()


class LogoutView(AuthenticateView):

    templatePath = 'logout'
    minorNavigationItem = '/logout/'

    def getResponse(self, redirectPath=''):
        self.redirectPath = redirectPath
        self.stopSession()
        return super(LogoutView, self).getResponse()


def login(request, returnPath=''):
    return LoginView(request=request).getResponse(returnPath)

def logout(request, redirect=''):
    return LogoutView(request=request).getResponse(redirect)

