from django.conf.urls import url

from functools import wraps
import re, inspect

def route(path, name=None, prefix=''):
    def wrap(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        if not hasattr(wrapper, '__routes__'):
            wrapper.__routes__ = []

        wrapper.__routes__.insert(0, dict(path=path, name=name, prefix=prefix))
        
        return wrapper
    return wrap

class EasyRoute(object):
    _repl = {
        'int': r'(?P<{paramname}>\d+)',
        'str': r'(?P<{paramname}>[^/]+)',
        'float': r'(?P<{paramname}>\d+(\.\d+)?)',
        'bool': r'(?P<{paramname}>[01tfTF]|[Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])',
    }
    _syntax = re.compile(r'\<(?P<paramname>[A-Za-z0-9_]+)(:(?P<type>[A-Za-z0-9]+))?\>')

    def __init__(self, prefix=''):
        self.prefix = prefix or ''

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._build_urls()

        return self._urls

    def _build_urls(self):
        self._urls = []
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for n, m in members:
            if hasattr(m, '__routes__'):
                self.__register(getattr(self, n))

    def __register(self, fn):
        routes = fn.__routes__
        for route in routes:
            path = route.get('path', None)
            name = route.get('name', None)
            prefix = route.get('prefix', self.prefix)

            items = path.split('/')
            r = []
            for i in items:
                m = EasyRoute._syntax.match(i)
                if m is not None:
                    paramname = m.group("paramname")
                    typ = m.group('type') or "str"
                    typ = typ.lower()
                    if not typ in EasyRoute._repl:
                        raise TypeError("{} is not a supported type for EasyRoute".format(typ))

                    r.append(EasyRoute._repl[typ].format(paramname=paramname))
                else:
                    r.append(i)
            self._urls.append(url(r'^' + r'/'.join(r) + r'$', fn, name=name, prefix=prefix))
