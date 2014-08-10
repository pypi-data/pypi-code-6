import threading


_thread_local = threading.local()


def get_request():
    return getattr(_thread_local, 'current_django_request', None)


def _set_request(value):
    _thread_local.current_django_request = value


class StoreRequestMiddleware(object):
    def process_request(self, request):
        _set_request(request)

    def process_response(self, request, response):
        _set_request(None)
        return response

    # Note: do not clear the request in process_exception() - we want the request details in the error message logged
    # by "django.request" and process_response() gets called later anyway.
