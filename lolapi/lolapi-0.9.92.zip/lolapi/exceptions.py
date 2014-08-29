# -*- coding: utf-8 -*-

# General exceptions


class UnsupportedRegion(Exception):
    """ Raised if the API requests a resource in a region it does not support. """
    pass


# HTTP response code exceptions

class BadRequest(Exception):
    """ Raised on HTTP 400 response code. """
    pass


class Unauthorized(Exception):
    """ Raised on HTTP 401 response code. """
    pass


class NotFound(Exception):
    """ Raised on HTTP 404 response code. """
    pass


class RateLimitExceeded(Exception):
    """ Raised on HTTP 429 response code. """
    pass


class InternalServerError(Exception):
    """ Raised on HTTP 500 response code. """
    pass


class ServiceUnavailable(Exception):
    """ Raised on HTTP 503 response code. """
    pass


class HttpResponseHandler(object):
    """
    Used to map HTTP response codes to exceptions.
    """

    def __init__(self):
        self.exceptions = {
            400: BadRequest,
            401: Unauthorized,
            404: NotFound,
            429: RateLimitExceeded,
            500: InternalServerError,
            503: ServiceUnavailable
        }

    def handle(self, request):
        exception = self.exceptions.get(request.status_code)
        if exception:
            try:
                raise exception(request.json()['status']['message'])
            except ValueError:
                raise exception()