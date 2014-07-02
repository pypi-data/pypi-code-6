
from . import version

VERSION = version.VERSION
__version__ = VERSION


from .api import Request, File
from .api import init, api_key, base_url
from .api import get_filters, apply_image_filters

import logging
try:
    # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
