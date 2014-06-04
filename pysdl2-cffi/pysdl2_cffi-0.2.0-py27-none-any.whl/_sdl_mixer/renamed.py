# "pretty" names without the NAMESPACE_ prefixes...
from __future__ import absolute_import

from _sdl_mixer import lib
__all__ = []

def _init():
    here = globals()
    import re
    constant = re.compile("MIX_[A-Z][A-Z]+")
    for name in dir(lib):
        if constant.match(name):
            pretty_name = name[4:]
        elif not name.startswith("Mix_"):
            continue
        else:
            pretty_name = name[4].lower() + name[5:]
        here[pretty_name] = getattr(lib, name)
        __all__.append(pretty_name)
        __all__.sort()

_init()
