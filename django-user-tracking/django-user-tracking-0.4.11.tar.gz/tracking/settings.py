
from django.conf import settings
from django.conf import global_settings

TRACKING_BOGUS_IP = getattr(settings, 'TRACKING_BOGUS_IP', '10.10.10.10')
NO_TRACKING_PREFIXES = getattr(settings, 'NO_TRACKING_PREFIXES', [])

"""
Tracking timeout is set to 10 minutes by default.
"""
TRACKING_TIMEOUT = getattr(settings, 'TRACKING_TIMEOUT', '10')

"""
Tracking clean-up timeout is set to 24 hours by default.
"""
TRACKING_CLEANUP_TIMEOUT = getattr(settings, 'TRACKING_CLEANUP_TIMEOUT', 24)

DEFAULT_TRACKING_TEMPLATE = getattr(settings,
                                    'DEFAULT_TRACKING_TEMPLATE',
                                    'tracking/visitor_map.html')
USE_GEOIP = getattr(settings, 'TRACKING_USE_GEOIP', False)
CACHE_TYPE = getattr(settings, 'GEOIP_CACHE_TYPE', 4)

STATIC_URL = getattr(settings, 'STATIC_URL', global_settings.STATIC_URL)
MEDIA_URL = getattr(settings, 'MEDIA_URL', global_settings.MEDIA_URL)
