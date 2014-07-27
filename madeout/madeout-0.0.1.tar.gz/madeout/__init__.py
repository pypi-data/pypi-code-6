import requests
import types
from urlparse import urlparse


class URL:

    def __init__(self, url):
        self._pages_cache = {}
        self.parsed_url = urlparse(url)
        self.scheme = self.parsed_url.scheme

        if not self.scheme:
            raise ValueError('Missing scheme in url')

        if self.scheme  not in ('http', 'https'):
            raise ValueError('Invalid scheme')

        self.hostname = self.parsed_url.hostname

        for name in self.hostname.split('.'):
            if len(name) < 2:
                raise ValueError('Invalid url: %s' % url )

    @property
    def url(self):
        return "%s://%s" % (self.scheme, self.hostname)

    def get(self, path, force=False):
        if not path.starts_with('/'):
            path = '/' + path

        if not path in self._pages_cache or force:
            url = self.url + path
            self._pages_cache[path] = requests.get(url)

        return self._pages_cache[path]


class Result:

    def __init__(self, **kwargs):
        self.desc = kwargs.get('desc', '')
        self.result = kwargs.get('result')


class BaseInspector:

    def __init__(self, url):
        self.url = URL(url)
        self.results = []

    def get(self, path):
        return self.url.get(path)

    def execute(self):
        self.results = []
        methods = dir(self)
        for method in methods:
            if method.startswith('check_'):
                self._execute_method_by_name(method)

    def _execute_method_by_name(self, method_name):
        method = getattr(self, method_name)
        if type(method) is types.MethodType:
            result = Result(desc=method.__doc__, result=method())
            self.results.append(result)


class Inspector(BaseInspector):
    pass
