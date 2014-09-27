# encoding: utf-8

import urlparse
import re
import os
import sys
import os.path

try:
    import requests
except ImportError:
    print('Please install requests.')
    sys.exit()

import pyocean
from .exceptions import *


class ApiClient(object):
    """The base class for the other classes in this package.
    """

    end_point = 'https://api.digitalocean.com/v2/'

    def __init__(self):
        self.access_token = os.getenv('PYOCEAN_ACCESS_TOKEN')

    def call_api(self, path, method='get', params=None, data=None):
        """Call the DigitalOcean API.

        Keyword arguments:
        path   -- The endpoint of the API, relative to: 
                  https://api.digitalocean.com/v2/ 
        method -- The HTTP method (get, post, put, delete).
        params -- The query string.
        data   -- The request body.

        """
        adapter = requests.adapters.HTTPAdapter(max_retries=0)
        sess = requests.Session()
        sess.mount('http', adapter)
        try:
            headers = {}
            if self.access_token:
                headers['Authorization'] = 'Bearer %s' % self.access_token
            f = getattr(sess, method.lower())
            r = f(urlparse.urljoin(self.end_point, path), 
                  headers=headers, params=params, data=data)
        except requests.exceptions.RequestException as e:
            if type(e) is requests.exceptions.ConnectionError:
                print('ERROR: connection failed.')
            elif type(e) is requests.exceptions.ProxyError:
                print('ERROR: proxy error.')
            elif type(e) is requests.exceptions.Timeout:
                print('ERROR: request timed out.')
            elif type(e) is requests.exceptions.SSLError:
                print('ERROR: SSL error occured.')
            sys.exit()
        else:
            try:
                content = r.json()
            except:
                content = {}
            status_code = int(r.status_code)
            if status_code >= 500:
                raise ServerError(content.get('message'), status_code)
            elif status_code >= 400:
                raise ClientError(content.get('message'), status_code)
            return content


class Resource(ApiClient):
    """This class represents a single resource in the API.
    """

    def __init__(self, attrs, parent=None):
        """Initialization.

        Keyword arguments:
        attrs  -- A dict containing the attributes for the object. This dict 
                  is the JSON object returned from the API.
        parent -- The ID of the parent object. For example, the Domain object
                  is the parent of DomainRecord object.
        """
        super(Resource, self).__init__()
        self._attrs = attrs if type(attrs) is dict else {}
        self._parent = parent
        self._json_key = None
        self._classname = self.__class__.__name__
        self._resource = '%ss' % self._classname.lower()

    def __getattr__(self, name):
        """Convenient method to access the object attributes.
        """
        if name in self._attrs:
            return self._attrs[name]
        else:
            msg = "'%s' object has no attribute '%s'." % (self._classname, name)
            raise AttributeError(msg)

    def all(self):
        """Returns all objects.
        """
        return getattr(pyocean, '%sIterator' % self._classname)()

    def get(self, resource_id):
        """Returns a single object.
        """
        data = self.call_api('%s/%s' % (self._resource, str(resource_id)))
        key = self._json_key or self._resource[:-1]
        return getattr(pyocean, self._classname)(data[key])

    def create(self, attrs):
        """Create a new object.
        """
        data = self.call_api(self._resource, method='post', data=attrs)
        key = self._json_key or self._resource[:-1]
        return getattr(pyocean, self._classname)(data[key])

    def destroy(self):
        """Destroy an object.
        """
        if self._attrs.get('id'):
            path = '%s/%s' % (self._resource, self._attrs['id'])
            data = self.call_api(path, method='delete')
        else:
            raise ValueError('Droplet is not loaded.')


class ResourceIterator(ApiClient):
    """This class represents a collection of resources from the API.
    """

    def __init__(self, parent=None):
        super(ResourceIterator, self).__init__()
        self._parent = parent
        self._data = []
        self._page = 1
        self._has_more = True
        self._json_key = None
        self._classname = re.sub('Iterator$', '', self.__class__.__name__)
        self._resource = '%ss' % self._classname.lower()

    def __iter__(self):
        return self

    def next(self):
        if not self._data and self._has_more:
            content = self.call_api(self._resource, params={'page': self._page})
            try:
                key = self._json_key or \
                      os.path.basename(re.sub('/\d+', '', self._resource))
                self._data = content[key]
            except KeyError:
                self._data = None
            try:
                self._has_more = bool(content['links']['pages']['next'])
            except KeyError:
                self._has_more = False
            self._page += 1

        if self._data:
            attrs = self._data.pop(0)
            class_ = getattr(pyocean, self._classname)
            return class_(attrs, self._parent) if self._parent else class_(attrs)
        else:
            raise StopIteration
