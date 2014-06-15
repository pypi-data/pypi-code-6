"""Context processors
==================

cms_enabled
-------------

Lo skeleton di base installa ``jmb.core.context_processors.cms_enabled`` per
personalizzare ``base.html``. Questo aggiunge al context la variabile dei
settings :var:`CMS_ENABLED`

"""

from django.conf import settings

def admin_theme_less(request):
    return {'ADMIN_THEME_LESS': settings.ADMIN_THEME_LESS}

def cms_enabled(request):
    return {'CMS_ENABLED': settings.CMS_ENABLED}
