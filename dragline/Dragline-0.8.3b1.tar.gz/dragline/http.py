from urllib import urlencode
import socket
from hashlib import sha1
import time
import httplib2
from defaultsettings import RequestSettings


class RequestError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Request:

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
    method = "GET"
    form_data = None
    headers = {}
    callback = None
    meta = None
    retry = 0

    def __init__(self, url, method="GET", form_data=None, headers={}, callback=None, meta=None,):
        self.url = url
        if method:
            self.method = method
        if callback:
            self.callback = callback
        if meta:
            self.meta = meta
        if form_data:
            self.form_data = form_data
        if headers:
            self.headers = headers

    def _set_state(self, state):
        self.__dict__ = state

    def __str__(self):
        return self.get_unique_id(False)

    def usha1(self, x):
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
            http = httplib2.Http(cache=self.settings.CACHE, timeout=timeout)
            req_headers = self.settings.HEADERS
            req_headers.update(self.headers)
            headers, content = http.request(
                self.url, self.method, form_data, req_headers)
            res = Response(self.url, content, headers, self.meta)
            end = time.time()
            if not headers.fromcache and self.settings.AUTOTHROTTLE:
                self.updatedelay(end, start)
                time.sleep(Request.settings.DELAY)
        except (httplib2.ServerNotFoundError, socket.timeout, socket.gaierror) as e:
            raise RequestError(e.message)
        return res

    def get_unique_id(self, hashing=True):
        request = self.method + ":" + self.url
        if self.form_data:
            request += ":" + urlencode(
                {i: j for i, j in sorted(self.form_data.items(),
                                         key=lambda t: t[0])})
        if hashing:
            return self.usha1(request)
        else:
            return request

    @classmethod
    def updatedelay(cls, end, start):
        delay = end - start
        cls.settings.DELAY = min(
            max(cls.settings.MIN_DELAY, delay,
                (cls.settings.DELAY + delay) / 2.0),
            cls.settings.MAX_DELAY)


class Response:

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

    def __init__(self, url=None, body=None, headers=None, meta=None):
        self.url = url
        self.body = body
        self.headers = headers
        self.meta = meta
