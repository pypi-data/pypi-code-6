import logging
import sys

import django
from django.core.handlers.wsgi import WSGIHandler, set_script_prefix
try:
    from django.core.handlers.base import get_script_name
except ImportError:
    from django.core.handlers.wsgi import get_script_name
from django.core.urlresolvers import resolve
from django import http

from .conf import urlconf

logger = logging.getLogger('django.request')


class WebSocketHandler(WSGIHandler):
    """
    We can use pretty much all of Django's request handling code,
    we just need to set the custom urlconf.
    """
    
    def get_response(self, request):
        request.urlconf = urlconf
        if 'wsgi.websocket' not in request.META:
            logger.warning('Bad Request (No WebSocket Upgrade)',
                exc_info=sys.exc_info(),
                extra={
                    'status_code': 400
                }
            )
            return http.HttpResponseServerError('You must access this using a WebSocket.')
            
        return super(WebSocketHandler, self).get_response(request)

def get_wsgi_websocket_application():
    if hasattr(django, 'setup'):
        django.setup()
    return WebSocketHandler()