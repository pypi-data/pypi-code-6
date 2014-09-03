# "pretty" names without the NAMESPACE_ prefixes...
from __future__ import absolute_import

import _sdl.renamer
from . import lib

def _init():
    # as an alternative, these names could go straight into sdl/__init__.py
    # allowed even though they don't start with prefix:
    whitelist = ['SDLError',
                 'Struct',
                 'ffi']
    here = globals()
    import re
    constant_re = re.compile("(SDL_)(?P<pretty_name>[A-Z][A-Z].+)$")
    renamer = _sdl.renamer.Renamer(lib, "SDL_", constant_re, whitelist)
    for name in dir(lib):
        value = getattr(lib, name)
        pretty_name = renamer.rename(name, value)
        if not pretty_name:
            continue
        here[pretty_name] = value

_init()
