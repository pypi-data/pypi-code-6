import abc
from apy.http import Response
from apy.container import Parameters, Services


class Controller:
    def __init__(self, request, parameters=None, services=None):
        """
        @type request: apy.http.Request
        @type parameters: apy.container.Parameters
        @type services: apy.container.Services
        """
        if parameters is None:
            parameters = Parameters()
        if services is None:
            services = Services(parameters=parameters)

        self._request = request
        self._parameters = parameters
        self._services = services


class ErrorHandler(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def get_not_found_response(request):
        """ @type request: apy.http.Request """

    @staticmethod
    @abc.abstractmethod
    def get_internal_server_error_response(request):
        """ @type request: apy.http.Request """


class DefaultErrorHandler(ErrorHandler):
    @staticmethod
    def get_not_found_response(request):
        response = Response()
        response.set_status(404)
        response.data = 'Not found'
        return response

    @staticmethod
    def get_internal_server_error_response(request):
        response = Response()
        response.set_status(500)
        response.data = 'Internal Server Error'
        return response
