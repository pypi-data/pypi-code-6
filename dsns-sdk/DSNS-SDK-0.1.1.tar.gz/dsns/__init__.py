import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    AUTH_TOKEN = getattr(settings, "DSNS_SECRET_KEY")
    HOST = getattr(settings, "DSNS_HOST")
except AttributeError, e:
    raise ImproperlyConfigured(
        "App 'dsns' is not configured properly: %s" % e.message)

from dsns.api import DSNS
