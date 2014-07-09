"""Mirador API client

.. moduleauthor:: Nick Jacob <nick@mirador.im>

"""
from __future__ import absolute_import

import base64
import requests
from requests import exceptions as req_exp
from .errors import http_exceptions, MiradorException
from .result import MiradorResult


class MiradorClient(object):
    """Interface for the Mirador API

    Simple interface for retrieving results from the
    Mirador API. Returns [MiradorResult] on all method
    """

    API_BASE = "http://api.mirador.im"
    CLASSIFY_ENDPOINT = "/v1/classify"
    HEADERS = {
        'User-Agent': 'MiradorClient/1.0 Python'
    }

    MAX_LEN = 2

    def __init__(self, api_key, timeout=10):
        """Instaniate a MiradorClient
        Args:
            api_key: the mirador api key (string)
            timeout: timeout for API access (default: 10 seconds)

        Returns:
            A MiradorClient instance
        """

        self._api_key = api_key
        self._url = "{0}{1}".format(
            self.API_BASE, self.CLASSIFY_ENDPOINT
        )

    def _params(self, data, method):
        """prepare paramters for the request"""

        key = 'data' if method == 'post' else 'params'
        data['api_key'] = self._api_key

        return {
            'headers': self.HEADERS,

            # data is of the appropraite key
            key: data,

            # set the timeout to a factor of the # pix
            'timeout': self._timeout(len(data))
        }

    def _timeout(self, num_pix):
        return (float(num_pix) * 2.75)

    def _prepare_request(self, **data):
        """prepare the options & parameters of request"""

        if not data or ('image' not in data and 'url' not in data):
            raise http_exceptions[400]("url(s) or image(s) required")

        # assign the correct method based on type
        method = 'get' if not 'image' in data else 'post'
        params = self._params(data, method)

        return method, params

    def _request(self, **data):
        """make the request via requests module"""

        method, params = self._prepare_request(**data)

        try:
            r = getattr(requests, method)(self._url, **params)
        except req_exp.ConnectionError:
            raise MiradorException(
                "could not connect to server: check your network connection",
                400
            )
        except req_exp.HTTPError:
            raise http_exceptions[
                (r.status_code if r else 500)
            ]("unexpected error")
        except req_exp.Timeout:
            raise http_exceptions[500](
                "Timeout occurred. Try again with fewer request objects"
            )

        if r.status_code != 200:
            raise http_exceptions[r.status_code](r.text)

        return r.json() if r.text else {}

    def _read_image(self, image):
        """read an image if it's a file and return the name"""

        if isinstance(image, basestring):
            with open(image, 'rb') as imf:
                return image, imf.read()
        else:
            return image.name, image.read()

    def _prepare_image(self, im_f):
        """convert an image name or file into base64 encoded string"""

        name, data = self._read_image(im_f)

        if not data:
            raise http_exceptions[400]("no image data for: {}".format(name))
        return name, base64.b64encode(data)

    def _chunk_and_flatten(self, fn, L):
        res = [
            fn(*L[i:i + self.MAX_LEN])
            for i in xrange(0, len(L), self.MAX_LEN)
        ]

        # flatten the results
        return [x for sl in res for x in sl]

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

        if len(urls) > self.MAX_LEN:
            return self._chunk_and_flatten(self.classify_urls, urls)

        if isinstance(urls[0], (list, tuple)):
            urls = urls[0]

        res = self._request(url=urls)

        return MiradorResult.parse_results(
            urls, res.get('results', None)
        )

    def classify_raw(self, buffers):
        """Classify raw strings representing the files
        Args:
            buffers: {filenames => strings} of raw image data
        Returns:
            lit of MiradorResult objects
        """
        if not buffers:
            return []

        res = self._request(
            image=map(
                lambda b: base64.b64encode(b).replace("\n", ''),
                buffers.values()
            )
        )

        return MiradorResult.parse_results(
            buffers.keys(), res.get('results', None)
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

        filedata = map(self._prepare_image, files)

        res = self._request(
            image=map(lambda x: x[1], filedata)
        )

        return MiradorResult.parse_results(
            map(lambda x: x[0], filedata), res.get('results', None)
        )
