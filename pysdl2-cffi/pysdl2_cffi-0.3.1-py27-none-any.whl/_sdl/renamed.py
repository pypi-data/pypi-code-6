# "pretty" names without the NAMESPACE_ prefixes...
from __future__ import absolute_import

from . import lib

def _init():
    # as an alternative, these names could go straight into sdl/__init__.py
    # allowed even though they don't start with prefix:
    whitelist = ['SDLError',
                 'Struct',
                 'ffi']
    here = globals()
    import re
    constant = re.compile("(SDL_)(?P<pretty_name>[A-Z][A-Z].+)$")
    for name in dir(lib):
        value = getattr(lib, name)
        pretty_name = name
        match = constant.match(name)
        if name.startswith('SDLK'):
            pretty_name = name[3:]
        elif not name.startswith('SDL_'):
            if not name in whitelist:
                continue
        elif isinstance(value, type):
            pretty_name = name[4:]
        elif match:
            pretty_name = match.group('pretty_name')
        else:
            pretty_name = name[4].lower() + name[5:]
        here[pretty_name] = value

_init()