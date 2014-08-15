
from exceptions import *

from core import *

import android, googlevoice, ios5, ios6, ios7, jsoner, tabular, xmlmms

try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution("smstools").version
except pkg_resources.DistributionNotFound:
    __version__ = "unknown version"
