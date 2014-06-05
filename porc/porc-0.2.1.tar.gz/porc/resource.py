import json
import requests
from requests_futures.sessions import FuturesSession
import copy
import re
from .version import VERSION
try:
    # python 2
    from urllib import quote
except ImportError:
    # python 3
    from urllib.parse import quote

URL_PATTERNS = [
    "(?P<collection>.+)/(?P<key>.+)/relations/(?P<kinds>.+)",
    "(?P<collection>.+)/(?P<key>.+)/events/(?P<type>.+)",
    "(?P<collection>.+)/(?P<key>.+)/refs/(?P<ref>.+)",
    "(?P<collection>.+)/(?P<key>.+)",
    "(?P<collection>.+)"
]

RESPONSE_PATTERNS = [
    "/v0/(?P<collection>.+)/(?P<key>.+)/events/(?P<type>.+)/(?P<timestamp>\d+)/(?P<ordinal>\d+)",
    "/v0/(?P<collection>.+)/(?P<key>.+)/refs/(?P<ref>.+)"
]

class Resource(object):

    """
    Ancestor for all Orchestrate resources.
    Handles storing URL state, headers, sessions, etc.

    If you create an object, like a `Client`, then use that to
    create a `Collection` object, the `Collection` will inherit any options
    from the `Client` object, such as auth settings.

    Likewise, all objects inheriting from Resource can make HTTP requests
    using the methods `head`, `get`, `put`, `post`, and `delete`,
    even if Orchestrate would only return a `405 Method Not Allowed`
    for a given method.
    """
    def __init__(self, uri, **kwargs):
        self.uri = uri

        # if given an existing session, use it
        if kwargs.get('session'):
            self._session = kwargs['session']
            del kwargs['session']
        # set the resource's session as either sync or async
        # according to keyword arguments
        elif kwargs.get('async') == False:
            self._session = requests.Session()
            del kwargs['async']
        # default to async
        else:
            self._session = FuturesSession()

        # set path parameters according to given url
        self._set_path()

        # pass remaining kwargs as defaults to requests
        self._set_options(**kwargs)

    def _init_child(self, child_obj, *path, **kwargs):
        """
        Create child objects from the resource's current settings.
        Used to create descendent resources, ex: keys from collections
        """
        if len(path):
            uri = self.uri + '/' + '/'.join([quote(path_elem) for path_elem in path])
        else:
            uri = self.uri

        # merge current and new settings into a new dict
        opts = dict(self.opts, **kwargs)
        # if both the parent and child have a callback, wrap them together
        if 'background_callback' in self.opts and 'background_callback' in kwargs:
            def callback(session, response):
                self.opts['background_callback'](session, response)
                kwargs['background_callback'](session, response)
            opts['background_callback'] = callback

        return child_obj(uri, session=self._session, **opts)

    def _set_path(self):
        """
        Set the path variable with params like $collection, etc.
        based on the object's URI
        """
        start_after_segment = 'api.orchestrate.io/v0/'
        start_after_index = self.uri.find(
            start_after_segment) + len(start_after_segment)
        path = self.uri[start_after_index:]
        for regex in URL_PATTERNS:
            match = re.match(regex, path)
            if match:
                self.path = match.groupdict()
                # handle relations with multiple kind parameters
                if 'kinds' in self.path:
                    self.path['kinds'] = self.path['kinds'].split('/')
                break
        else:
            self.path = dict()

    def _set_options(self, **kwargs):
        """
        Sets header defaults and updates them with given kwargs
        """
        # set defaults
        if not hasattr(self, 'opts'):
            self.opts = {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'python-requests/1.2.0 porc/%s' % VERSION
                }
            }
        # merge passed kwargs into opts
        if kwargs:
            self.opts.update(kwargs)

    def _make_request(self, method, body={}, **headers):
        """
        Executes the request based on the given body and headers
        along with options set on the object.
        """
        # create a copy of options so we can mess with it
        opts = copy.copy(self.opts)

        # normalize `params` kwarg according to method
        if body:
            if method in ['head', 'get', 'delete']:
                if type(body) == dict:
                    # convert True and False to true and false
                    for key, value in list(body.items()):
                        if value == True:
                            body[key] = 'true'
                        elif value == False:
                            body[key] = 'false'
                opts['params'] = body
            else:
                opts['data'] = json.dumps(body)

        # auto-quote headers like if-match
        for header in ['If-Match', 'If-None-Match']:
            if header in headers:
                # wrap in quotes if not already surrounded
                if headers[header][0] != '"':
                    headers[header] = '"%s"' % headers[header]
        # update opts with headers following any modifications
        opts['headers'].update(headers)

        # make the request
        if type(self._session) == FuturesSession:
            # handle multiple background_callbacks
            if 'background_callback' in opts:
                background_callback = opts['background_callback']
                def callback(session, response):
                    background_callback(session, response)
                    self._handle_response(session, response)
                del opts['background_callback']
            else:
                callback = self._handle_response
            future = getattr(self._session, method)(
                self.uri, background_callback=callback, **opts)
            return future
        else:
            response = self._session.request(method, self.uri, **opts)
            self._handle_response(None, response)
            return response

    def _handle_response(self, session, response):
        """
        Modifies the response, normalizing headers and the like
        """
        response.path = dict()
        for regex in RESPONSE_PATTERNS:
            # check location
            location_match = re.match(
                regex, response.headers.get('location', ''))
            # if not in location, try content-location
            if not location_match:
                location_match = re.match(
                    regex, response.headers.get('content-location', ''))
            # else, try the etag
            if not location_match:
                location_match = re.match('"(?P<ref>.+)-gzip"', response.headers.get('ETag', ''))
            # if a match was found in either place, attach it to the `path`
            # attribute
            if location_match:
                response.path = location_match.groupdict()
                break

    def head(self, querydict={}, **headers):
        """
        Make a HEAD request against the object's URI.
        `querydict` is a mapping object, like a dict, 
        that is serialized into the querystring.
        Any keyword arguments are passed along as headers.
        """
        return self._make_request('head', querydict, **headers)

    def get(self, querydict={}, **headers):
        """
        Make a GET request against the object's URI.
        `querydict` is a mapping object, like a dict, 
        that is serialized into the querystring.
        Any keyword arguments are passed along as headers.
        """
        return self._make_request('get', querydict, **headers)

    def put(self, body={}, **headers):
        """
        Make a PUT request against the object's URI.
        `querydict` is a mapping object, like a dict, 
        that is serialized into the querystring.
        Any keyword arguments are passed along as headers.
        """
        return self._make_request('put', body, **headers)

    def post(self, body={}, **headers):
        """
        Make a POST request against the object's URI.
        `querydict` is a mapping object, like a dict, 
        that is serialized into the querystring.
        Any keyword arguments are passed along as headers.
        """
        return self._make_request('post', body, **headers)

    def delete(self, querydict={}, **headers):
        """
        Make a DELETE request against the object's URI.
        `querydict` is a mapping object, like a dict, 
        that is serialized into the querystring.
        Any keyword arguments are passed along as headers.
        """
        return self._make_request('delete', querydict, **headers)
