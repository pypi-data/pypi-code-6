from zope.interface import Interface, Attribute, implements

class ILogin(Interface):
    user = Attribute("Session username")
    id = Attribute("User id")
    hc = Attribute("Hit counter")
    admin = Attribute("Is admin")

class Login(object):
    implements(ILogin)

    def __init__(self, session):
        self.user = None
        self.id = None
        self.admin = False
        self.hc = 0 
