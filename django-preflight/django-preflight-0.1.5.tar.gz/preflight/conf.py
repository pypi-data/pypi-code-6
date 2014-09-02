from django.conf import settings


BASE_TEMPLATE = getattr(
    settings, 'PREFLIGHT_BASE_TEMPLATE', "admin/base.html")
TABLE_CLASS = getattr(settings, 'PREFLIGHT_TABLE_CLASS', "listing")
ENABLE_SETTINGS = getattr(settings, 'PREFLIGHT_ENABLE_SETTINGS', False)
