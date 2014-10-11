# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2011
from __future__ import with_statement

from six.moves import http_cookiejar as cookielib
import gzip
from six import BytesIO, PY2
from six.moves import urllib
from types import MethodType

from . import __version__
from .utils import json
from .form import MultiPartForm

__all__ = ['getAPI', 'API']

def getAPI(url, cj=None):
    return API(url, cj)

class API(object):
    __version__ = __version__
    __name__ = 'ox'
    DEBUG = False
    debuglevel = 0

    def __init__(self, url, cj=None):
        if cj:
            self._cj = cj
        else:
            self._cj = cookielib.CookieJar()
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cj),
                                            urllib.request.HTTPHandler(debuglevel=self.debuglevel))
        self._opener.addheaders = [
            ('User-Agent', '%s/%s' % (self.__name__, self.__version__))
        ]

        self.url = url
        r = self._request('api', {'docs': True})
        self._properties = r['data']['actions']
        self._actions = r['data']['actions'].keys()
        for a in r['data']['actions']:
            self._add_action(a)

    def _add_method(self, method, name):
        if name is None:
            name = method.func_name
        if PY2:
            setattr(self, name, MethodType(method, self, type(self)))
        else:
            setattr(self, name, MethodType(method, self))

    def _add_action(self, action):
        def method(self, *args, **kw):
            if not kw:
                if args:
                    kw = args[0]
                else:
                    kw = None
            return self._request(action, kw)
        if 'doc' in self._properties[action]:
            method.__doc__ = self._properties[action]['doc']
        if PY2:
            method.func_name = str(action)
        else:
            method.func_name = action
        self._add_method(method, action)

    def _json_request(self, url, form):
        result = {}
        try:
            body = form.body()
            if PY2:
                if not isinstance(url, bytes):
                    url = url.encode('utf-8')
                request = urllib.request.Request(url)
                request.add_data(body)
            else:
                request = urllib.request.Request(url, data=body, method='POST')
            request.add_header('Content-Type', form.get_content_type())
            request.add_header('Content-Length', str(len(body)))
            request.add_header('Accept-Encoding', 'gzip, deflate')
            f = self._opener.open(request)
            result = f.read()
            if f.headers.get('content-encoding', None) == 'gzip':
                result = gzip.GzipFile(fileobj=BytesIO(result)).read()
            result = result.decode('utf-8')
            return json.loads(result)
        except urllib.error.HTTPError as e:
            if self.DEBUG:
                import webbrowser
                if e.code >= 500:
                    with open('/tmp/error.html', 'w') as f:
                        f.write(e.read())
                    webbrowser.open_new_tab('/tmp/error.html')

            result = e.read()
            try:
                result = result.decode('utf-8')
                result = json.loads(result)
            except:
                result = {'status':{}}
            result['status']['code'] = e.code
            result['status']['text'] = str(e)
            return result
        except:
            if self.DEBUG:
                import webbrowser
                import traceback
                traceback.print_exc()
                if result:
                    with open('/tmp/error.html', 'w') as f:
                        f.write(str(result))
                    webbrowser.open_new_tab('/tmp/error.html')
            raise

    def _request(self, action, data=None):
        form = MultiPartForm()
        form.add_field('action', action)
        if data:
            form.add_field('data', json.dumps(data))
        return self._json_request(self.url, form)

