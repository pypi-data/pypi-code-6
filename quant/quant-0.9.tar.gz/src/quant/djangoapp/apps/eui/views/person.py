from dm.view.base import *
from quant.djangoapp.apps.eui.views.base import QuantView
from quant.djangoapp.apps.eui.views import manipulator
import quant.command
import random

class PersonView(AbstractClassView, QuantView):

    domainClassName = 'Person'
    majorNavigationItem = '/persons/'
    minorNavigationItem = '/persons/'

    def __init__(self, **kwds):
        super(PersonView, self).__init__(**kwds)
        self.person = None

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Index', 'url': '/persons/'},
            {'title': 'Search', 'url': '/persons/search/'},
        ]
        if self.session:
            self.minorNavigation.append(
                {
                    'title': 'API Key', 
                    'url': '/persons/%s/apikey/' % self.session.person.name
                }
            )
        else:
            self.minorNavigation.append(
                {
                    'title': 'Join', 
                    'url': '/persons/create/'
                }
            )

           
    def isSshPluginEnabled(self):
        if not hasattr(self, '_isSshPluginEnabled'):
            self._isSshPluginEnabled = 'ssh' in self.registry.plugins
        return self._isSshPluginEnabled

    def setContext(self):
        super(PersonView, self).setContext()
        self.context.update({
            'person'         : self.getDomainObject(),
        })

    def getDomainObject(self):
        super(PersonView, self).getDomainObject()
        self.person = self.domainObject
        return self.person

class PersonClassView(PersonView): pass

class PersonListView(PersonClassView, AbstractListView):

    templatePath = 'persons/list'

    def canAccess(self):
        return self.canReadPerson()


class PersonSearchView(PersonClassView, AbstractSearchView):

    templatePath = 'persons/search'
    minorNavigationItem = '/persons/search/'
    
    def canAccess(self):
        return self.canReadPerson()


class PersonCreateView(PersonClassView, AbstractCreateView):

    templatePath = 'persons/create'
    minorNavigationItem = '/persons/create/'

    def getManipulatorClass(self):
        return manipulator.PersonCreateManipulator

    def canAccess(self):
        return self.canCreatePerson()
        
    def setContext(self):
        super(PersonCreateView, self).setContext()
        if self.dictionary[self.dictionary.words.CAPTCHA_IS_ENABLED]:
            captchaHash = self.captcha.name
            captchaUrl = self.makeCaptchaUrl(captchaHash)
            self.context.update({
                'isCaptchaEnabled'  : True,
                'captchaHash'       : captchaHash,
                'captchaUrl'        : captchaUrl,
            })
        else:
            self.context.update({
                'isCaptchaEnabled'  : False,
            })

    def makePostManipulateLocation(self):
        return '/login/'


class PersonInstanceView(PersonView):

    def canUpdatePerson(self):
        if self.person == None:
            self.getDomainObject()
        return super(PersonInstanceView, self).canUpdatePerson()


class PersonReadView(PersonInstanceView, AbstractReadView):

    templatePath = 'persons/read'

    def getDomainObject(self):
        if self.path == '/persons/home/' and self.session:
            self.domainObject = self.session.person
            self.person = self.domainObject
        else:
            super(PersonReadView, self).getDomainObject()
        if self.session and self.session.person == self.domainObject:
            self.majorNavigationItem = '/persons/home/'
            self.minorNavigationItem = '/persons/home/'
        return self.domainObject

    def canAccess(self):
        if not self.getDomainObject():
            return False
        return self.canReadPerson()

    def setContext(self):
        super(PersonReadView, self).setContext()
        self.context.update({
            'isSessionPerson': self.isSessionPerson()
        })

    def isSessionPerson(self):
        if self.session and self.domainObject:
            return self.session.person == self.domainObject
        else:
            return False


class PersonUpdateView(PersonInstanceView, AbstractUpdateView):

    templatePath = 'persons/update'

    def getManipulatorClass(self):
        return manipulator.PersonUpdateManipulator

    def canAccess(self):
        if not self.getDomainObject():
            return False
        return self.canUpdatePerson()

    def makePostManipulateLocation(self):
        return '/persons/home/'


class PersonDeleteView(PersonInstanceView, AbstractDeleteView):

    templatePath = 'persons/delete'
    
    def canAccess(self):
        if not self.getDomainObject():
            return False
        return self.canDeletePerson()

    def manipulateDomainObject(self):
        super(PersonDeleteView, self).manipulateDomainObject()
        if self.session:
            if self.getDomainObject() == self.session.person:
                self.stopSession()

    def makePostManipulateLocation(self):
        return '/persons/'


class PersonApiKeyView(PersonReadView):

    templatePath = 'persons/apikey'
   
    def getMinorNavigationItem(self):
        return '/persons/%s/apikey/' % self.session.person.name
    
    def canAccess(self):
        if not self.getDomainObject():
            return False
        return self.canUpdatePerson()

    def setContext(self):
        super(PersonInstanceView, self).setContext()
        apiKeys = self.registry.apiKeys.findDomainObjects(person=self.session.person)
        if apiKeys:
            apiKey = apiKeys[0]
        else:
            apiKey = self.registry.apiKeys.create(person=self.session.person)
        self.context.update({
            'apiKeyString': apiKey.key
        })


def list(request):
    view = PersonListView(request=request)
    return view.getResponse()
    
def search(request, startsWith=''):
    view = PersonSearchView(request=request, startsWith=startsWith)
    return view.getResponse()
    
def create(request, returnPath=''):   
    view = PersonCreateView(request=request)
    return view.getResponse()

def read(request, personName=''):
    view = PersonReadView(request=request, domainObjectKey=personName)
    return view.getResponse()

def update(request, personName):
    view = PersonUpdateView(request=request, domainObjectKey=personName)
    return view.getResponse()

def delete(request, personName):
    view = PersonDeleteView(request=request, domainObjectKey=personName)
    return view.getResponse()

def apikey(request, personName):
    view = PersonApiKeyView(request=request, domainObjectKey=personName)
    return view.getResponse()

