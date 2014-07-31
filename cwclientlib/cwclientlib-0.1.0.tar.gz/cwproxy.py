# -*- coding: utf-8 -*-

"""A CWProxy class wraps a CubicWeb repository.

>>> import cwproxy
>>> p = cwproxy.CWProxy('https://www.cubicweb.org')
>>> a = p.rql('Any X,T WHERE X is Project, X title T')
>>> print(a.json())
...

"""

import json
import requests
import hmac
import hashlib
from datetime import datetime

CONTENT_TYPE = {'json': 'application/json',
                'form': 'application/x-www-form-urlencoded'}

RQLIO_API = '1.0'

class SignedRequestAuth(requests.auth.AuthBase):
    """Auth implementation for CubicWeb with cube signedrequest"""

    HEADERS_TO_SIGN = ('Content-MD5', 'Content-Type', 'Date')

    def __init__(self, token_id, secret):
        self.token_id = token_id
        self.secret = secret

    def __call__(self, req):
        if req.body:
            req.headers['Content-MD5'] = hashlib.md5(req.body).hexdigest()
        content_to_sign = (req.method
                           + req.url
                           + ''.join(req.headers.get(field, '')
                                     for field in self.HEADERS_TO_SIGN))
        content_signed = hmac.new(self.secret, content_to_sign).hexdigest()
        req.headers['Authorization'] = 'Cubicweb %s:%s' % (self.token_id,
                                                           content_signed)
        return req

def build_request_headers(ctype='json'):
    headers = {'Accept': 'application/json',
               'Content-Type': CONTENT_TYPE[ctype],
               'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}
    return headers

class CWProxy(object):
    """CWProxy wraps a CubicWeb repository and access it via HTTP.
    """

    def __init__(self, base_url, auth=None, verify=None):
        self.base_url = base_url.strip().rstrip('/')
        self.auth = auth
        self._ssl_verify = verify
        self._default_vid = 'jsonexport' # OR 'ejsonexport'?

    def rql(self, rql, vid=None):
        """Perform an urlencoded POST to /view with rql=<rql>
        """
        if rql.split()[0] in ('INSERT', 'SET', 'DELETE'):
            raise ValueError('You must use the rqlio() method to make write RQL queries')
        params = {'url': self.base_url + '/view',
                  'headers': build_request_headers('form'),
                  'verify': self._ssl_verify,
                  'auth': self.auth,
                  'data': {'rql': rql,
                           'vid': vid if vid else self._default_vid,
                           'fallbackvid': '404'},
                  }
        return requests.post(**params)

    def rqlio(self, queries):
        """Multiple RQL for reading/writing data from/to a CW instance.
        """
        params = {'url': '/'.join([self.base_url, 'rqlio', RQLIO_API]),
                  'headers': build_request_headers('json'),
                  'verify': self._ssl_verify,
                  'auth': self.auth,
                  'data': json.dumps(queries),
                  }
        return requests.post(**params)
