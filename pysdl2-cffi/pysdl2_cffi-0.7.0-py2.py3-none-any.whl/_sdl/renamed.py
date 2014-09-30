# "pretty" names without the NAMESPACE_ prefixes...
from __future__ import absolute_import

import _sdl.renamer
from . import lib

__all__ = []

def _mapping():
    # as an alternative, these names could go straight into sdl/__init__.py
    # allowed even though they don't start with prefix:
    whitelist = ['SDLError', 'Struct', 'ffi']
    import re
    constant_re = re.compile("(SDL_)(?P<pretty_name>[A-Z][A-Z].+)$")
    renamer = _sdl.renamer.Renamer(lib, "SDL_", constant_re, whitelist)
    for name in dir(lib):
        value = getattr(lib, name)
        pretty_name = renamer.rename(name, value)
        if not pretty_name:
            continue
        yield name, pretty_name

def _init():
    # XXX use apipkg here?
    here = globals()
    for name, pretty_name in _mapping():
        here[pretty_name] = getattr(lib, name)
        __all__.append(pretty_name)
    __all__.sort()

_init()
