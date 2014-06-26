import json
import re

import requests


class ResourceManager(object):

    def __init__(self, client):
        self.client = client


class BaseAPI(object):

    def __init__(self):
        self.resources = {getattr(sc, '__resourcename__', cc_to_uc(sc.__name__)): sc
                          for sc in ResourceManager.__subclasses__()}

    def resource_factory(self, resource):
        """Factory function to get a resource manager instance

        :param resource: name of the resource
        :returns: resource manager class object
        :rtype: subclass of ResourceManager

        """
        return self.resources[resource]

    def for_resource(self, resource):
        """Get the resource manager instance for the resource

        :param resource: resource name
        :returns: resource manager instance
        :rtype: subclass of ResourceManager

        """
        raise NotImplementedError


class JSONRequests(object):

    def __init__(self, base_url, client=requests):
        self.base_url = base_url
        self._client = client

    def url(self, path):
        """Builds the absolute url from the path

        :param str path: path section of the url
        :returns: absolute url with base_url and path
        :rtype: string

        """
        return '{}{}'.format(self.base_url, path)

    def request(self, method, path, expected_statuses, *args, **kwargs):
        """Sends request to the server and returns the response

        :param str method: name of the method
        :param str path: path of the resource url
        :param set expected_statuses: set of expected status codes
        :returns: response from the api
        :rtype: json decoded value

        """
        f = getattr(self._client, method)
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        headers = {'content-type': 'application/json'}
        r = f(self.url(path), headers=headers, *args, **kwargs)
        if r.status_code in expected_statuses:
            if r.status_code != 204:
                return r.json()
        else:
            raise JSONRequestError(r)

    def get(self, path, *args, **kwargs):
        """Sends a get request and returns response

        :param str path: url path
        :returns: response of the get request
        :rtype: json decoded value
        :raises: JSONRequestError if status is not 200

        """
        return self.request('get', path, {200}, *args, **kwargs)

    def post(self, path, data, *args, **kwargs):
        """Sends a post request and returns the response

        :param str path: url path
        :param data: data to send in the post request
        :type data: json serializable value
        :returns: response of the post request
        :rtype: json decoded value
        :raises: JSONRequestError if status is not one of 201,202

        """
        kwargs['data'] = data
        return self.request('post', path, {201, 202}, *args, **kwargs)

    def put(self, path, data, *args, **kwargs):
        """Sends a put request and returns the response

        :param str path: url path
        :param data: data to send in the put request
        :type data: list of dict (or anything json serializable)
        :returns: response of the put request
        :rtype: json decoded value
        :raises: JSONRequestError if status is not one of 200,201,202

        """
        kwargs['data'] = data
        return self.request('put', path, {200, 201, 202}, *args, **kwargs)

    def patch(self, path, data, *args, **kwargs):
        """Sends a patch request and returns the response

        :param str path: url path
        :param data: data to send in the patch request
        :type data: json serializable value
        :returns: response of the patch request
        :rtype: json decoded value
        :raises: JSONRequestError if status is not one of 200,202

        """
        kwargs['data'] = data
        return self.request('patch', path, {200, 202}, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        """Sends a delete request to the API

        :param str path: url path
        :returns: response of the delete request
        :rtype: NoneType or json decoded value
        :raises: JSONRequestError if status is not one of 202,204

        """
        return self.request('delete', path, {202, 204}, *args, **kwargs)


class JSONRequestError(Exception):

    def __init__(self, response):
        """Request error exception for JSON requests

        Raised when the frontend api responds with a non desirable
        status code

        :param response: response object (from requests lib)

        """
        try:
            resp = response.json()
        except ValueError:
            reason = 'The API endpoint responded with an error'
        else:
            reason = resp.get('reason', 'The API endpoint responded with an error')
        msg = '{} ({})'.format(reason, response.status_code)
        Exception.__init__(self, msg)


def cc_to_uc(s):
    """Converts a CamelCase string to underscore or snake_case

    :param str s: CamelCase string
    :returns: snake_case string
    :rtype: str

    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
