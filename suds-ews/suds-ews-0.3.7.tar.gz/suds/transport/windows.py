import urllib2

from suds.transport import https

class HttpAuthenticated(https.HttpAuthenticated):
    def __init__(self, **kwargs):
        from ntlm import HTTPNtlmAuthHandler

        https.HttpAuthenticated.__init__(self, **kwargs)
        self.pm = urllib2.HTTPPasswordMgrWithDefaultRealm()
        self.handler = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(self.pm)
        self.urlopener = urllib2.build_opener(self.handler)

    def send(self, request):
        credentials = self.credentials()
        if not (None in credentials):
            u = credentials[0]
            p = credentials[1]
            self.pm.add_password(None, request.url, u, p)

        return https.HttpAuthenticated.send(self, request)
