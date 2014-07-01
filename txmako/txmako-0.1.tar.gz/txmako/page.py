import os

from twisted.web import static, server, resource, client
from twisted.web.util import redirectTo
from twisted.internet import defer

from mako.template import Template
from mako.lookup import TemplateLookup

from txmako import session

class Page(resource.Resource):
    addSlash = True
    templateDir = 'templates'
    loginRequired = False
    adminRequired = False

    def __init__(self, config=None, *a, **kw):
        self.config = config
        resource.Resource.__init__(self, *a, **kw)
        self.childPages = self.setChildren()

    def setChildren(self):
        return {}

    def getChild(self, name, request):
        if not name:
           return self

        try:
            return self.childPages[name]
        except:
            return resource.Resource.getChild(self, name, request)

    def renderTemplate(self, data):
        tlookup = TemplateLookup(directories=[self.templateDir])

        templatePath = os.path.join(self.templateDir, self.template)

        template = Template(filename=templatePath,
            module_directory='template.cache', lookup=tlookup)

        return template.render(**data)

    def renderPage(self, request):
        # Stuff happens here. Return a dict, or string if no template
        
        return {}

    def render_GET(self, request):
        if self.loginRequired:
            login = self.getLogin(request)
            if not login.id:
                #No session info - redirect to login
                return redirectTo(self.loginPage+'?from=%s'%request.path, request) 

        if self.adminRequired:  
            login = self.getLogin(request)
            if not login.admin:
                request.setResponseCode(403)
                return "Access denied"
                
        renDeferred = defer.maybeDeferred(self.renderPage, request)
        
        renDeferred.addCallback(self.completeRequest, request)
        renDeferred.addErrback(self.logError, request)
        
        return server.NOT_DONE_YET

    def render_POST(self, request):
        # These are handled the same - although semantically ugly
        return self.render_GET(request)

    def logError(self, error, request):                                                                                                                       
        error.printTraceback()
        request.setResponseCode(500)
        request.write('Error 500')
        request.finish()

    def completeRequest(self, response, request):
        # Complete deferred request
        if self.template:
            if isinstance(response, dict):
                
                if self.loginRequired:
                    # If this page requires a login then give the template the
                    # session object as well
                    login = self.getLogin(request)
                    response['login'] = login

                # Render the template and write the result encoded with utf-8
                request.write(self.renderTemplate(response).encode('utf-8'))
            else:
                request.write(response)
        else:
            request.write(response)
            
        request.finish()

    def getLogin(self, request):
        s = request.getSession()
        return session.ILogin(s)
