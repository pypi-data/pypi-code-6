# -*- coding: utf-8 -*-

__docformat__ = "restructuredtext en"

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

RQLIO_API = '1.0'

class SignedRequestAuth(requests.auth.AuthBase):
    """Auth implementation for CubicWeb with cube signedrequest"""

    HEADERS_TO_SIGN = ('Content-MD5', 'Content-Type', 'Date')

    def __init__(self, token_id, secret):
        self.token_id = token_id
        self.secret = secret

    def __call__(self, req):
        content = ''
        if req.body:
            content = req.body
        req.headers['Content-MD5'] = hashlib.md5(content).hexdigest()
        content_to_sign = (req.method
                           + req.url
                           + ''.join(req.headers.get(field, '')
                                     for field in self.HEADERS_TO_SIGN))
        content_signed = hmac.new(self.secret, content_to_sign).hexdigest()
        req.headers['Authorization'] = 'Cubicweb %s:%s' % (self.token_id,
                                                           content_signed)
        return req

def build_request_headers():
    headers = {'Accept': 'application/json',
               'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}
    return headers

class RemoteValidationError(Exception):
    pass

class CWProxy(object):
    """CWProxy: A simple helper class to ease building CubicWeb_
    clients. It allows to:

    * execute RQL_ queries remotely (using rqlcontroller_),
    * access instances that requires authentication (using signedrequest_).

.. _CubicWeb: http://www.cubicweb.org/
.. _RQL: http://docs.cubicweb.org/annexes/rql/language
.. _rqlcontroller: http://www.cubicweb.org/project/cubicweb-rqlcontroller/
.. _signedrequest: http://www.cubicweb.org/project/cubicweb-signedrequest/
    """

    def __init__(self, base_url, auth=None, verify=None):
        self.base_url = base_url.strip().rstrip('/')
        self.auth = auth
        self._ssl_verify = verify
        self._default_vid = 'jsonexport' # OR 'ejsonexport'?

    def rql(self, rql, path='view', **data):
        """Perform an urlencoded POST to /<path> with rql=<rql>
        """
        if rql.split()[0] in ('INSERT', 'SET', 'DELETE'):
            raise ValueError('You must use the rqlio() method to make write RQL queries')

        data.setdefault('vid', self._default_vid)
        if path == 'view':
            data.setdefault('fallbackvid', '404')
        if rql:
            data['rql'] = rql

        params = {'url': self.base_url + '/' + path,
                  'headers': build_request_headers(),
                  'verify': self._ssl_verify,
                  'auth': self.auth,
                  'data': data,
                  }
        return requests.post(**params)

    def rqlio(self, queries):
        """Multiple RQL for reading/writing data from/to a CW instance.

        :queries: list of queries, each query being a couple (rql, args)

        Example:

          queries = [('INSERT CWUser U: U login %(login)s, U upassword %(pw)s',
                      {'login': 'babar', 'pw': 'cubicweb rulez & 42'}),
                     ('INSERT CWGroup G: G name %(name)s',
                      {'name': 'pachyderms'}),
                     ('SET U in_group G WHERE G eid %(g)s, U eid %(u)s',
                      {'u': '__r0', 'g': '__r1'}),
                     ('INSERT File F: F data %(content)s, F data_name %(fname)s',
                      {'content': BytesIO('some binary data'),
                       'fname': 'toto.bin'}),
                    ]
          self.rqlio(queries)

        """
        headers = build_request_headers()
        files = self.preprocess_queries(queries)

        params = {'url': '/'.join([self.base_url, 'rqlio', RQLIO_API]),
                  'headers': headers,
                  'verify': self._ssl_verify,
                  'auth': self.auth,
                  'files': files,
                  }
        posted = requests.post(**params)
        if posted.status_code == 500:
            cause = posted.json()
            if 'reason' in cause:
                # was a RemoteCallFailed
                raise RemoteValidationError(cause['reason'])
        return posted

    def preprocess_queries(self, queries):
        """Pre process queries arguments to replace binary content by
        files to be inserted in the multipart HTTP query

        Any value that have a read() method will be threated as
        'binary content'.

        In the RQL query, binary value are replaced by unique '__f<N>'
        references (the ref of the file object in the multipart HTTP
        request).
        """

        files = {}
        for i, (rql, args) in enumerate(queries):
            for k, v in args.items():
                if hasattr(v, 'read') and callable(v.read):
                    # file-like object
                    args[k] = '__f%s' % i
                    files[args[k]] = v
        files['json'] = json.dumps(queries)
        return files

