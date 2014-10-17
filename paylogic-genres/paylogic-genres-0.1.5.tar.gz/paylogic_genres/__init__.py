"""Paylogic genres Python library."""

import os


def get_supported_languages():
    """Get supported i18n languages."""
    basedir = os.path.join(os.path.dirname(__file__), 'locale')
    return [
        unicode(name) for name in os.listdir(basedir)
        if os.path.isdir(os.path.join(basedir, name))
    ]
