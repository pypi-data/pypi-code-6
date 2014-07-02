import httplib2
import base64
import json
import datetime


class EasyAPI(object):
    def _make_request(self, action, method, body=None):
        raise NotImplementedError("You must implement this method")

    def convert_datetime(self, val):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = val - epoch

        return int(delta.total_seconds() * 1000.0)

    @property
    def api(self):
        _make_request = self._make_request
        _get_type = "GET"
        _update_type = "PUT"
        _create_type = "POST"
        _delete_type = "DELETE"

        class api_object(object):
            def __init__(self, parent=None):
                self._object_name = parent

            def __repr__(self):
                return self.__str__()

            def __str__(self):
                return str(_make_request(self._object_name, _get_type))

            def __call__(self):
                return self.__repr__()

            def __getattr__(self, name):
                """Return an object that allows for Accessing, Updating, and Deleting a specific object type based off of the name parameter.
                """
                actual_name = "%s/%s" % (self._object_name, name) if self._object_name else name

                class api_list():
                    _object_name = actual_name
                    _get = None

                    @property
                    def get(self):
                        """Get object/objects and caches the response

                        Python call: 
                        >>> my_api_service.api.foo
                        
                        API call: 
                        GET http://yourapi.com/foo
                        """
                        self._get = _make_request(self._object_name, _get_type) if not self._get else self._get

                        return self._get

                    def __getattr__(self, name):
                        return api_object("%s/%s" % (self._object_name, name))

                    def __str__(self):
                        return str(self.get)

                    def __repr__(self):
                        return self.__str__()

                    def __call__(self):
                        return self.__repr__()

                    def __len__(self):
                        if not isinstance(self.get, list):
                            raise TypeError("This object is not iterable")

                        return len(self.get)

                    def __iter__(self):
                        if not isinstance(self.get, list):
                            raise TypeError("This object is not iterable")

                        return iter(self.get)

                    def __getitem__(self, key):
                        """Get a list of objects and cache the response

                        Python call: 
                        >>> my_api_service.api.foo['bar']
                        
                        API call: 
                        GET http://yourapi.com/foo/bar
                        """
                        return api_object("%s/%s" % (self._object_name, key))

                    def __setitem__(self, key, value):
                        """Update the item specified by the key to the one with the value.

                        Python call:
                        >>> my_api_service.api.foo['bar'] = my_updated_object

                        API call:  
                        PUT http://yourapi.com/foo/bar
                        """
                        return _make_request("%s/%s" % (self._object_name, key), _update_type, json.dumps(value))

                    def __delitem__(self, key):
                        """Update the item specified by the key to the one with the value.

                        Python call:
                        >>> del(my_api_service.api.foo['bar'])

                        API call:  
                        DELETE http://yourapi.com/foo/bar
                        """
                        return _make_request("%s/%s" % (self._object_name, key), _delete_type)

                    def append(self, value):
                        """Add an item

                        Python call:
                        >>> my_api_service.api.foo.add(my_new_object)

                        API call:  
                        POST http://yourapi.com/foo/bar
                        """
                        return _make_request("%s" % (self._object_name), _create_type, json.dumps(value))

                    def put(self, value):
                        """Add an item

                        Python call:
                        >>> my_api_service.api.foo.add(my_new_object)

                        API call:  
                        PUT http://yourapi.com/foo/bar
                        """
                        return _make_request("%s" % (self._object_name), _update_type, json.dumps(value))

                return api_list()

        return api_object()


class BasicAuthentication(object):
    _user = None
    _password = None
    _log = False

    def __init__(self, username=None, password=None, base_url='v2', ca_certs=None, log=False):
        self._user = username
        self._password = password
        self._base_url = base_url
        self._ca_certs = ca_certs
        self._log = log

    def _make_request(self, action, method, body=None):
        http = httplib2.Http(ca_certs='/etc/ssl/certs/ca-certificates.crt')
        http.add_credentials(self._user, self._password)

        auth = base64.encodestring("%s:%s" % (self._user, self._password))
        headers = {
            'Authorization': 'Basic %s' % auth,
            'Content-Type': 'application/json',
            'Accept': 'application/json'}

        url = "%s/%s" % (self._base_url, action)
        url = "%s/" % url if url[-1] != '/' else url

        if self._log:
            import logging
            logger = logging.getLogger(__name__)
            logger.debug('url: %s' % url)
            logger.debug('method: %s' % method)
            logger.debug('body: %s' % body)

        response, content = http.request(url, method=method, body=body, headers=headers)

        if self._log:
            logger.debug('response: %s' % response)
            logger.debug('content: %s' % content)

        status = response['status']

        # Error statuses
        if status == '404':
            raise KeyError
        if status == '500':
            raise RuntimeError

        # OK statuses
        if status == '204':
            return {}
        if status == '200':
            return json.loads(content)
