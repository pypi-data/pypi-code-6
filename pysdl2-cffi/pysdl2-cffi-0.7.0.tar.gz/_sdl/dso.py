# dlopen the SDL library.

import sys

from .cdefs import ffi

# strategy from cairocffi
def dlopen(ffi, *names):
    """Try various names for the same library, for different platforms."""
    for name in names:
        try:
            return ffi.dlopen(name)
        except OSError:
            pass
    # Re-raise the exception.
    if sys.platform == "win32":
        bitness = getattr(sys, 'maxsize', getattr(sys, 'maxlength', 0)).bit_length()+1
        raise OSError("""Unable to load %s.\n\nMake sure you have downloaded SDL 2.0.x, SDL_image, SDL_mixer, and SDL_ttf DLLs from https://libsdl.org/ ; place them on PATH or in the current directory. This Python interpreter requires the %d-bit libraries.""" % (names[1], bitness))
    return ffi.dlopen(names[0]) # pragma: no cover

_LIB = dlopen(ffi,
              'SDL2',
              'SDL2.dll',
              'libSDL2.so',
              'libSDL2-2.0.so.0')
