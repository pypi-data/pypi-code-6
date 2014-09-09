# dlopen the SDL library.

from _sdl.dso import dlopen
from .cdefs import ffi

_LIB = dlopen(ffi,
              'SDL2_ttf',
              'SDL2_ttf.dll',
              'libSDL2_ttf.so',
              'libSDL2_ttf-2.0.so.0')
