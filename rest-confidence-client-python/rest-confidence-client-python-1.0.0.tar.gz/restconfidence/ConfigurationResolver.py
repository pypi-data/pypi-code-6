import urllib
import urllib2

class ConfigurationResolver:
    """
    rest-confidence client

    resolver = ConfigurationResolver("http://localhost:8000")
    print resolver.load()
    print resolver.load("key2")
    print resolver.load("key2/limit")

    resolver = ConfigurationResolver("http://localhost:8000", {"env": "production"})
    print resolver.load("key2")
    """
    def __init__(self, configurationServerUrl="http://localhost", opts=None):
        self.configurationServerUrl = configurationServerUrl
        self.opts = opts
        self.filters = urllib.urlencode(opts) if opts else None

    def _prepare_request(self, url):
        request = urllib2.Request(url)
        request.add_header('content-type', 'application/json')
        request.add_header('user-agent', 'python rest-confidence client')

        return request

    def load(self, property=""):
        url = self.configurationServerUrl + "/" + property

        if self.filters:
            url += "?" + self.filters

        request = self._prepare_request(url)

        try:
            return urllib2.urlopen(request).read()
        except urllib2.URLError as err:
            print "Unable to connect with %s" % self.configurationServerUrl, err

if __name__ == "__main__":
    resolver = ConfigurationResolver()
    print resolver.load()

    resolver = ConfigurationResolver("http://5.255.150.56:8000")
    print resolver.load()
    print resolver.load("key2")
    print resolver.load("key2/limit")

    resolver = ConfigurationResolver("http://5.255.150.56:8000", {"env": "production"})
    print resolver.load("key2")
