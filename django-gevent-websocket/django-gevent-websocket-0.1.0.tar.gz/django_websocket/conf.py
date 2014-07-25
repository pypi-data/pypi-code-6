from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

try:
    urlconf = settings.WEBSOCKET_URLCONF
except AttributeError:
    raise ImproperlyConfigured('You must provide a WEBSOCKET_URLCONF value in your settings.')

try:
    server = settings.WEBSOCKET_SERVER
except AttributeError:
    server = ''