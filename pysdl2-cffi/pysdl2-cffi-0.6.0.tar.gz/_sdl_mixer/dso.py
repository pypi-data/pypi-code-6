# dlopen the SDL library.

from _sdl.dso import dlopen
from .cdefs import ffi

_LIB = dlopen(ffi,
              'SDL2_mixer',
              'SDL2_mixer.dll',
              'libSDL2_mixer-2.0.so',
              'libSDL2_mixer-2.0.so.0')
