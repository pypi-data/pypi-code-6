"""Mirador API client

.. moduleauthor:: Nick Jacob <nick@mirador.im>

"""
from __future__ import absolute_import

import base64
import requests
from .errors import http_exceptions, MiradorException
from .result import MiradorResult


def import_async_requests():
    try:
        from grequests import async
        return async
    except ImportError:
        try:
            from requests import async
            return async
        except ImportError:
            pass

        raise MiradorException(
            "grequests async library required for asynchronous requests"
        )


class MiradorClient(object):
    """Interface for the Mirador API

    Simple interface for retrieving results from the
    Mirador API. Returns [MiradorResult] on all method
    """

    API_BASE = "http://api.mirador.im"
    CLASSIFY_ENDPOINT = "/v1/classify"
    TIMEOUT = 10
    HEADERS = {
        'User-Agent': 'MiradorClient/1.0 Python'
    }

    def __init__(self, api_key, timeout=10):
        """Instaniate a MiradorClient
        Args:
            api_key: the mirador api key (string)
            timeout: timeout for API access (default: 10 seconds)

        Returns:
            A MiradorClient instance
        """

        self.TIMEOUT = timeout or self.TIMEOUT

        self._api_key = api_key
        self._url = "{0}{1}".format(
            self.API_BASE, self.CLASSIFY_ENDPOINT
        )

    def _params(self, data, method):
        """prepare paramters for the request"""

        key = 'data' if method == 'post' else 'params'
        data['api_key'] = self._api_key

        return {'headers': self.HEADERS, key: data}

    def _prepare_request(self, **data):
        """prepare the options & parameters of request"""
        if not data or ('image' not in data and 'url' not in data):
            raise http_exceptions[400]("url(s) or image(s) required")

        method = 'get' if not 'image' in data else 'post'
        params = self._params(data, method)

        return method, params

    def _request(self, **data):
        """make the request via requests module"""

        method, params = self._prepare_request(**data)
        r = getattr(requests, method)(self._url, **params)

        if r.status_code != 200:
            raise http_exceptions[r.status_code](r.text)
        return r.json()

    def _async_request(self, files_or_urls, on_done, **data):
        """make an asynchronous request to the API"""
        async = import_async_requests()

        # very basic callback that just
        # parses the response and hands it off
        # to the handler
        def handle_async_response(response):
            if response.status_code == 200:
                on_done(
                    MiradorResult.parse_results_safe(
                        files_or_urls,
                        response.json().get('results', None)
                    )
                )

        method, params = self._prepare_request(**data)

        # set up our response hook
        params['hooks'] = {'response': handle_async_response}
        r = getattr(async, method)(self._url, **params)

        # execute the request
        async.map([r])

    def _read_image(self, image):
        """read an image if it's a file and return the name"""

        if isinstance(image, basestring):
            with open(image, 'rb') as imf:
                return image, imf.read()
        else:
            return image.name, image

    def _prepare_image(self, im_f):
        """convert an image name or file into base64 encoded string"""

        name, data = self._read_image(im_f)

        if not data:
            raise http_exceptions[400]("no image data for: {}".format(name))
        return base64.b64encode(data)

    def classify_urls(self, *urls):
        """classifies url(s) via the API

        Args:
            *urls: urls to classify. Must be publically accessible
        Returns:
            a list of MiradorResult objects, each with three properties:
                name: a string representing the source url
                safe: boolean - is the image safe (unflagged)
                value: float representing confidence in flag result
        """
        if not urls:
            return []

        if isinstance(urls[0], (list, tuple)):
            urls = urls[0]

        res = self._request(url=urls)

        return MiradorResult.parse_results(
            urls, res.get('results', None)
        )

    def classify_files(self, *files):
        """classifies file(s) via the API
        Args:
            *files: filenames or file objects
        Returns:
            a list of MiradorResult objects, each with three properties:
                name: a string representing the source filename
                safe: boolean - is the image safe (unflagged)
                value: float representing confidence in flag result
        """
        if not files:
            return []

        if isinstance(files[0], (list, tuple)):
            files = files[0]

        res = self._request(
            image=map(self._prepare_image, files)
        )

        return MiradorResult.parse_results(
            files, res.get('results', None)
        )

    def async_classify_files(self, files, on_done):
        """asynchronously classify files, using `on_done` callback"""
        self._async_request(image=map(self._prepare_image, files))
