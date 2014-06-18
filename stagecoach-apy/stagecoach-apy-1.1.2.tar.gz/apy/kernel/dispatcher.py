import sys
from apy.kernel.routing import Router


class Dispatcher:
    def __init__(self, routes, application_parameters, application_services, error_handler):
        """
        @type routes: list or tuple
        @type application_parameters: apy.container.Parameters
        @type application_services: apy.container.Services
        @type error_handler: apy.handler.ErrorHandler
        """
        self._routes = routes
        self._application_parameters = application_parameters
        self._application_services = application_services
        self._error_handler = error_handler

    def _load_controller(self, module_class, request):
        """ @type request: apy.http.Request """
        module_name, class_name = module_class.rsplit('.', 1)
        __import__(module_name)
        module = sys.modules[module_name]
        controller_object = getattr(module, class_name)(request, self._application_parameters, self._application_services)
        return controller_object

    @staticmethod
    def _run_controller_method(controller, action_name, params=None):
        response = getattr(controller, action_name, lambda: None)(**params)
        return response

    def dispatch(self, request):
        """ @type request: apy.http.Request """
        router = Router(self._routes)
        result = router.match_request(request)

        if not result:
            return self._error_handler.get_not_found_response(request)

        module_class = result['controller']
        controller = self._load_controller(module_class, request)
        params = result['params']
        action_name = result['action']

        response = self._run_controller_method(controller, action_name, params)

        return response
