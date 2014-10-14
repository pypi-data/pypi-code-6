import re

from json_resource import ResourceNotFound
from flask import request


class Forbidden(Exception):
    """ Exception that is raised when an authorized request is disallowed.

    Will return a 403 response.
    """
    pass


class UnAuthorized(Exception):
    """ Exception that is raised when a request is no authorized.

    Will return a 401 response.
    """
    pass


class Authorization(object):
    """ Authorization base object.

    Extend this to implement custom authorization in your API.
    """

    def authorize(self, resource):
        """ Authorize `resource` against the request.

        Check if a method that corresponds to the request method exists on
        the object.

        If this method returns `True` the request is authorized. if the method
        returns `False`, the request is not allowed and a Forbidden error
        is raised.

        If no method corresponding to the request method exists, the `default`
        method is called.
        """
        try:
            func = getattr(self, request.method.lower())
        except:
            func = self.default

        if not func(resource):
            raise Forbidden('Access Denied')

    def default(self, resource):
        """ Default authorization method.

        This is called if no method corresponding to the request method exists.
        """
        pass


class TokenAuthorization(Authorization):
    """ Token Authorization base object.

    Extend this to implement token based authorization
    """
    token_class = None

    @property
    def token(self):
        """ Return the current token.

        Raises an Unauthorized error if no bearer token is supplied in the
        request.
        """
        header = request.headers.get('Authorization')

        try:
            token = re.match(
                r'^Bearer (?P<token>\w+)$', header
            ).group('token')
        except TypeError:
            raise UnAuthorized('Missing authorization header')
        except AttributeError:
            raise UnAuthorized('Invalid authorization header')

        try:
            return self.token_class({'access-token': token}).load()
        except ResourceNotFound:
            raise Forbidden('Invalid Access token')
