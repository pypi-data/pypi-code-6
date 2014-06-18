from __future__ import unicode_literals
import platform

try:
    from lacore.version import __version__
except ImportError:
    __version__ = "0.1.3.1"


def get_client_info(terse=False, withplatform=True):
    if terse is True:
        el = ["lacore"]
    else:
        el = ["Longaccess Python SDK"]
    el.append(__version__)
    if withplatform is True:
        el.append(platform.platform(True, terse))
        el.append("py"+platform.python_version())
        el.append(platform.machine())
    return " ".join(el)
# vim: et:sw=4:ts=4

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
