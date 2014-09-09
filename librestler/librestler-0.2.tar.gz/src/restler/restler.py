try:
    import urllib2
    from urlparse import urlparse
except ImportError:
    import urllib.request as urllib2
    from urllib.parse import urlparse
    from functools import reduce

from . import __version__
from .route import Route


class Restler(object):
    ''' Restler:
    RESTler is a wrapper around a web app API.  It sets the base URL and allows
    for attribute/OO based access to the RESTful URLs.

    ex.
    >> github = Restler('http://api.github.com/')
    >> github
    'Restler: http://api.github.com/'
    >> github.user
    'Route: http://api.github.com/user/'
    >> github.user.username
    'Route: http://api.github.com/user/username/'
    '''
    __name__ = "Restler v{}".format(__version__)

    def __init__(self, base, cookies=False):
        ''' (constructor):
        '''
        self.EXCEPTION_THROWING = True  # set to False if you want return codes
        self.__test__ = False

        url_info = urlparse(base)
        scheme = url_info.scheme if len(url_info.scheme) else 'http'
        self.__url__ = '{}://{}'.format(scheme, url_info.netloc)
        self.__route_class = Route
        self.__route = self.__route_class(url_info.path, self)

        self.__opener__ = urllib2.build_opener()
        self.__opener__.addheaders = [('User-agent', self.__name__)]

        if cookies:  # `cookies` can be a bool, the CookieJar or CookiePolicy
            import cookielib
            if isinstance(cookies, cookielib.CookieJar):
                cj = cookies
            elif isinstance(cookies, cookielib.CookiePolicy):
                cj = cookielib.CookieJar(policy=cookies)
            else:
                cj = cookielib.CookieJar()

            self.__opener__.add_handler(urllib2.HTTPCookieProcessor(cj))

    def __call__(self, *args, **kwargs):
        ''' __call__:
        Acts as a call to the base URL `Route` for the application.
        '''
        return self.__route(*args, **kwargs)

    def __getattr__(self, attr):
        ''' __getattr__:
        Retrieves the existing method from the `Restler` object, if it does not
        exist, passes the attribute to the base route, returning any of it's
        existing methods or creates a child `Route` object for the new URL.

        Note: due to the existing method lookup, if your web API has a route
        for '[base URL]/base/', '[base URL]/base_class/', etc, they will not
        map properly as those are defined properties
        '''
        if attr in self.__dict__:
            return self.__dict__[attr]

        if attr.startswith('/'):
            if len(self.__route.__path__) > 0:
                if not attr.startswith(self.__route.__path__.rstrip('/')):
                    return attr
                attr = attr[len(self.__route.__path__):]

        return self.__route.__getattr__(attr.lstrip('/'))

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __repr__(self):
        return 'Restler: ' + str(self.__url__)

    def __str__(self):
        return str(self.__url__)

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)

    def __hash__(self):
        return reduce(lambda s, x: s ^ ord(x), str(self), 0)
