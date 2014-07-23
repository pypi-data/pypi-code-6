from __future__ import unicode_literals
from django.conf import settings

USER_SETTINGS = getattr(settings, 'CRAWLER_SETTINGS', None)

DEFAULTS = {
    'SITE_URL': 'http://localhost',
    'CACHE_TIMEOUT': 300,
}

crawler_settings = DEFAULTS.copy()
crawler_settings.update(USER_SETTINGS)
