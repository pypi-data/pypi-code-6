import gettext
from django.conf import settings
from django.utils import translation
from django.utils.translation import trans_real, get_language


def get_override_base():

    return getattr(settings, "PO_OVERRIDES",
                   "%s/var/locale" % settings.PROJECT_ROOT)


def generate_po_path(base, locale):

    return "%s/%s/LC_MESSAGES/django.po" % (base, locale)


def clear_trans_cache():

    try:
        # Reset gettext.GNUTranslation cache.
        gettext._translations = {}

        # Reset Django by-language translation cache.
        trans_real._translations = {}

        # Delete Django current language translation cache.
        trans_real._default = None

        translation.activate(get_language())

    except AttributeError:
        pass
