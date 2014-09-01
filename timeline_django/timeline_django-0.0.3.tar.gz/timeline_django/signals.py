from django.dispatch import Signal


wsgi_request_started = Signal(providing_args=['environ'])
wsgi_response_started = Signal(providing_args=['environ'])
