import logging
import sys
import re
from apy.kernel.routing import generate_routes
from apy.kernel.dispatcher import Dispatcher
from apy.kernel.conf import Settings
from apy.container import Parameters, Services


class Application:
    def __init__(self, environment='prod', config_dir='config'):
        settings = Settings(environment, config_dir)
        self._server_settings = settings.server

        if settings.debug is True:
            self._set_debug_logger()

        routes = generate_routes(settings.routes)

        error_handler = self._get_error_handler(settings.error_handler)

        parameters = Parameters(settings.parameters)
        services = Services(settings.services, parameters)

        self._dispatcher = Dispatcher(routes, parameters, services, error_handler)

        self._server_adapter = None
        if settings.server_adapter is not None:
            server_adapter_class = self._get_server_adapter_class(settings.server_adapter)
            self._server_adapter = server_adapter_class(self._server_settings, self._dispatcher, error_handler)

    def run_server(self):
        if self._server_adapter is None:
            raise ApplicationException('The server adapter is not configured yet.')
        self._server_adapter.run()

    def do_request(self, request):
        """
        @type request: apy.http.Request
        @rtype: apy.http.Response
        """
        return self._dispatcher.dispatch(request)

    @staticmethod
    def _set_debug_logger():
        logger = logging.getLogger('general')
        logger.setLevel(logging.DEBUG)

    @staticmethod
    def _get_server_adapter_class(server_adapter):
        server_adapter_module_class = server_adapter
        if re.match(r'^[A-Za-z0-9_]+$', server_adapter):
            server_adapter_module_class = 'apy.kernel.server.%s_adapter.ServerAdapter' % server_adapter
        module_name, class_name = server_adapter_module_class.rsplit('.', 1)
        __import__(module_name)

        module = sys.modules[module_name]
        return getattr(module, class_name)

    @staticmethod
    def _get_error_handler(error_handler_module_class):
        module_name, class_name = error_handler_module_class.rsplit('.', 1)
        __import__(module_name)
        module = sys.modules[module_name]
        return getattr(module, class_name)()


class ApplicationException(Exception):
    pass
