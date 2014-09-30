# dlopen the SDL library.

from _sdl.dso import dlopen
from .cdefs import ffi

_LIB = dlopen(ffi,
              'SDL2_image',
              'SDL2_image.dll',
              'libSDL2_image.so',
              'libSDL2_image-2.0.so.0')
