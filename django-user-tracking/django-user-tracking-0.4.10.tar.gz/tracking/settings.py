
from django.conf import settings


def get(key, default):
    getattr(settings, key, default)


TRACKING_TIMEOUT = 10  # seconds
TRACKING_BOGUS_IP = '10.10.10.10'
NO_TRACKING_PREFIXES = []
