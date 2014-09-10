from pkgutil import extend_path
from pkg_resources import declare_namespace

__path__ = extend_path(__path__, __name__)
declare_namespace(__name__)