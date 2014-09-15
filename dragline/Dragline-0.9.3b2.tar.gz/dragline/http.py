import six
if six.PY2:
    from urllib import urlencode
    from urlparse import urldefrag
else:
    from urllib.parse import urlencode
import socket
from hashlib import sha1
import time
import httplib2
from .defaultsettings import RequestSettings
from collections import defaultdict
import operator
import socks
from random import randint
from .redisds import Dict
import types
import re

socket.setdefaulttimeout(300)


class RequestError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Request(object):

    """
    :param url: the URL of this request
    :type url: string
    :param method: the HTTP method of this request. Defaults to ``'GET'``.
    :type method: string
    :param headers: the headers of this request.
    :type headers: dict
    :param callback: name of the function to call after url is downloaded.
    :type callback: string
    :param meta:  A dict that contains arbitrary metadata for this request.
    :type meta: dict
    """

    settings = RequestSettings()
    stats = Dict("stats:*")
    method = "GET"
    form_data = None
    headers = {}
    callback = None
    meta = None
    retry = 0
    cookies = None
    callback_object = None
    dontfilter = False
    _cookie_regex = re.compile('(([^ =]*)?=[^ =]*?;)')

    def __init__(self, url, method=None, form_data=None, headers=None, callback=None, meta=None, dontfilter=None):
        if isinstance(url, str):
            self.url = str(url)
        elif isinstance(url, unicode):
            self.url = unicode(url)
        else:
            AssertionError("Invalid url type")
        if method:
            assert method in ['GET', 'POST', 'HEAD', 'PUT', 'DELETE'], 'INVALID METHOD'
            self.method = method
        if callback:
            self.callback = callback
        if meta:
            self.meta = meta
        if form_data:
            self.form_data = {str(k): str(v)
                              for k, v in dict(form_data).items()}
        if headers:
            self.headers = headers
        if dontfilter:
            dontfilter = True

    def __getstate__(self):
        d = self.__dict__.copy()
        if isinstance(self.callback, types.MethodType) and hasattr(self.callback, 'im_self'):
            d['callback'] = self.callback.__name__
            if not Request.callback_object == self.callback.im_self:
                Request.callback_object = self.callback.im_self
        return d

    def __setstate__(self, d):
        if 'callback' in d and isinstance(d['callback'], str):
            d['callback'] = getattr(Request.callback_object, d['callback'])
        self.__dict__ = d

    def __repr__(self):
        return "<%s>" % self.get_unique_id(False)

    def __str__(self):
        return self.get_unique_id(False)

    def __usha1(self, x):
        """sha1 with unicode support"""
        if isinstance(x, unicode):
            return sha1(x.encode('utf-8')).hexdigest()
        else:
            return sha1(x).hexdigest()

    def send(self):
        """
        This function sends HTTP requests.

        :returns: response
        :rtype: :class:`dragline.http.Response`
        :raises: :exc:`dragline.http.RequestError`: when failed to fetch contents

        >>> req = Request("http://www.example.org")
        >>> response = req.send()
        >>> print response.headers['status']
        200

        """

        form_data = urlencode(self.form_data) if self.form_data else None
        try:
            start = time.time()
            timeout = max(self.settings.DELAY, self.settings.TIMEOUT)
            number = randint(0, len(self.settings.PROXIES))
            args = dict(disable_ssl_certificate_validation=True,
                        cache=self.settings.CACHE, timeout=timeout)
            if not number == 0:
                ip = self.settings.PROXIES[number - 1][0]
                proxy = self.settings.PROXIES[number - 1][1]
                args['proxy_info'] = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, ip, proxy)
            http = httplib2.Http(**args)
            http.follow_all_redirects = True
            req_headers = self.settings.HEADERS
            if self.settings.COOKIE:
                if Request.cookies:
                    req_headers.update({'Cookie': Request.cookies})
            req_headers.update(self.headers)
            headers, content = http.request(
                self.url, self.method, form_data, req_headers)

            if "set-cookie" in headers and not self.cookies:
                cookies = [i[0] for i in self._cookie_regex.findall(headers['set-cookie'])
                           if i[1].lower() not in ['domain']]
                Request.cookies = " ".join(cookies)

            res = Response(self.url, content, headers, self.meta)
            end = time.time()

            if not headers.fromcache and self.settings.AUTOTHROTTLE:
                self.updatedelay(end, start)
                time.sleep(self.settings.DELAY)
        except Exception as e:
            raise RequestError(e.message)
        else:
            self.stats.inc('pages_crawled')
            self.stats.inc('request_bytes', len(res))
        return res

    def get_unique_id(self, hashing=True):
        request = self.method + ":" + urldefrag(self.url)[0]
        if self.form_data:
            request += ":" + urlencode(sorted(self.form_data.items(),
                                              key=operator.itemgetter(1)))
        if hashing:
            return self.__usha1(request)
        else:
            return request

    @classmethod
    def updatedelay(cls, end, start):
        delay = end - start
        cls.settings.DELAY = min(
            max(cls.settings.MIN_DELAY, delay,
                (cls.settings.DELAY + delay) / 2.0),
            cls.settings.MAX_DELAY)


class Response(object):

    """
    This function is used to create user defined
    respones to test your spider and also in many
    other cases.
    :param url: the URL of this response
    :type url: string

    :param headers: the headers of this response.
    :type headers: dict

    :param body: the response body.
    :type body: str

    :param meta: meta copied from request
    :type meta: dict

    """
    url = None
    body = ""
    headers = {}
    meta = None
    status = None

    def __init__(self, url=None, body=None, headers=None, meta=None):
        if url:
            self.url = url
        if body:
            self.body = body
        if headers:
            self.headers = headers
            if 'status' in headers:
                self.status = headers['status']
            if 'content-location' in headers:
                self.url = headers['content-location']
        if meta:
            self.meta = meta

    def __str__(self):
        return "%s:%s" % (self.status, self.url)

    def __repr__(self):
        return "<%s>" % str(self)

    def __len__(self):
        if 'content-length' in self.headers:
            return int(self.headers['content-length'])
        return len(self.body)
