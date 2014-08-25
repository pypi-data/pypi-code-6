from quant.djangoapp.apps.eui.views.base import QuantView

class WelcomeView(QuantView):

    templatePath = 'welcome'
    minorNavigationItem = '/'

    def __init__(self, **kwds):
        super(WelcomeView, self).__init__(**kwds)

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Welcome', 'url': '/'},
        ]
        if self.session:
            self.minorNavigation.append(
                {'title': 'Log out',      'url': '/logout/'},
            )
        else:
            self.minorNavigation.append(
                {'title': 'Log in',      'url': '/login/'},
            )

    def canAccess(self):
        return self.canReadSystem()

    def setContext(self, **kwds):
        super(WelcomeView, self).setContext(**kwds)
        self.context.update({
        })


class PageNotFoundView(WelcomeView):

    templatePath = 'pageNotFound'

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Welcome', 'url': '/'},
        ]
        if self.session:
            self.minorNavigation.append(
                {'title': 'Help',       'url': '/help/'}
            )
        else:
            self.minorNavigation.append(
                {'title': 'Log in',      'url': '/login/'},
            )

class AccessControlView(QuantView):

    templatePath = 'accessDenied'
    minorNavigationItem = '/accessDenied/'

    def __init__(self, deniedPath='', **kwds):
        super(AccessControlView, self).__init__(**kwds)
        self.deniedPath = deniedPath

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Sorry', 'url': '/accessDenied/'},
        ]
    
    def canAccess(self):
        return self.canReadSystem()
        
    def setContext(self, **kwds):
        super(AccessControlView, self).setContext(**kwds)
        self.context.update({
            'deniedPath'  : self.deniedPath,
        })


class UserAccountView(QuantView):

    majorNavigationItem = '/persons/home/'

    def canAccess(self):
        return True

    def takeAction(self):
        if self.session:
            redirectPath = '/persons/%s/' % self.session.person.name
        else:
            redirectPath = '/login/'
        self.setRedirect(redirectPath)

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Welcome', 'url': '/'},
        ]
        if self.session:
            self.minorNavigation.append(
                {'title': 'Log out',     'url': '/logout/'}
            )
        else:
            self.minorNavigation.append(
                {'title': 'Log in',      'url': '/login/'},
            )


class RegistryWelcomeView(WelcomeView):

    templatePath = 'registry'
    majorNavigationItem = '/registry/'
    minorNavigationItem = '/registry/'

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Welcome', 'url': '/registry/'},
        ]


class TradesView(WelcomeView):

    templatePath = 'trades'
    majorNavigationItem = '/trades/'
    minorNavigationItem = '/trades/'

    def setMinorNavigationItems(self):
        from quant.djangoapp.apps.eui.views.registry import TradesNavigation
        self.minorNavigation = TradesNavigation(self).createMinorItems()


class CodesView(WelcomeView):

    templatePath = 'codes'
    majorNavigationItem = '/codes/'
    minorNavigationItem = '/codes/'

    def setMinorNavigationItems(self):
        from quant.djangoapp.apps.eui.views.registry import CodesNavigation
        self.minorNavigation = CodesNavigation(self).createMinorItems()


def welcome(request):
    view = WelcomeView(request=request)
    return view.getResponse()

def registry(request):
    view = RegistryWelcomeView(request=request)
    return view.getResponse()

def pageNotFound(request):
    view = PageNotFoundView(request=request)
    return view.getResponse()

def accessDenied(request, deniedPath):
    view = AccessControlView(request=request, deniedPath=deniedPath)
    return view.getResponse()

def user(request):
    view = UserAccountView(request=request)
    return view.getResponse()
 
def trades(request):
    view = TradesView(request=request)
    return view.getResponse()
 
def codes(request):
    view = CodesView(request=request)
    return view.getResponse()
 
