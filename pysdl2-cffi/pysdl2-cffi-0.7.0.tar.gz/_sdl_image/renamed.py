# "pretty" names without the NAMESPACE_ prefixes...
from __future__ import absolute_import
from _sdl_image import lib

__all__ = []

def _mapping():
    import re
    constant = re.compile("IMG_[A-Z][A-Z]+")
    for name in dir(lib):
        if not name.startswith("IMG_"):
            continue
        elif constant.match(name):
            pretty_name = name[4:]
        else:
            pretty_name = name[4].lower() + name[5:]
        yield name, pretty_name

def _init():
    here = globals()
    for name, pretty_name in _mapping():
        here[pretty_name] = getattr(lib, name)
        __all__.append(pretty_name)
    __all__.sort()

_init()