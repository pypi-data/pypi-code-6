from .computation_engine import apply, join, summarize, Engine, files_from
from .fs_cache import CacheBuilder
from .std_logger import get_logger

# DO NOT TOUCH THE FOLLOWING LINE:
import pkg_resources  # part of setuptools
__version__ = tuple(map(int, pkg_resources.require(__name__)[0].version.split(".")))
