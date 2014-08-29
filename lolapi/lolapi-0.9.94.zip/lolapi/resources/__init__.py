# -*- coding: utf-8 -*-

import requests
import urlparse

from ..exceptions import HttpResponseHandler, UnsupportedRegion


class Resource(object):
    """
    Common base class for all API resources.
    """

    def __init__(self, api):
        self._api = api
        self._scheme = u'https'
        self._netloc = u'%s.api.pvp.net' % self._api._region
        self._query = u'api_key=%s' % api._key
        self._response_handler = HttpResponseHandler()
        self._headers = {
            'Content-Type': 'application/json'
        }

    @property
    def _base_uri(self):
        return u'/'.join(['/api/lol', self._api._region, self._version])

    def _check_region(self):
        if not (self._api and self._api._region in self._available_regions):
            raise UnsupportedRegion()

    def _construct_url(self, path):
        """
        Builds the request url.
        urlparse expects 6 tuple:
        (scheme, netloc, path, params, query, fragment)

        :param path: URL path to request
        """
        path = map(unicode, path)  # cast everything as unicode for building url
        path = u'/'.join([self._base_uri] + path)
        args = (self._scheme, self._netloc, path, '', self._query, '')
        return unicode(urlparse.urlunparse(args))

    def _get(self, path):
        """
        Performs an HTTP GET request on the given path
        after verifying the resource region and SSL. Raises
        exception based on HTTP response code.

        :param path: URL path to request
        """
        url = self._construct_url(path)
        r = requests.get(url, verify=True, headers=self._headers)
        self._response_handler.handle(r)
        return r.json()