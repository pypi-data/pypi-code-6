# Handwritten helper methods for those hard-to-wrap functions.
# Overrides same-named functions from autohelpers.py

from .cdefs import ffi as _ffi
from .dso import _LIB
from .structs import unbox

def SDL_CalculateGammaRamp(a0, a1=_ffi.NULL):
    """void SDL_CalculateGammaRamp(float, uint16_t *)

    :param gamma: a gamma value where 0.0 is black and 1.0 is identity
    :param ramp: an array of 256 values filled in with the gamma ramp
    :return: ramp
    """
    if a1 == _ffi.NULL:
        a1 = _ffi.new("uint16_t[]", 256)
    _LIB.SDL_CalculateGammaRamp(a0, a1)
    return a1

def SDL_JoystickGetGUIDString(a0):
    """
    ``void SDL_JoystickGetGUIDString(SDL_JoystickGUID, char *, int)``

    Return a string representation for this guid. pszGUID must point to at
    least 33 bytes (32 for the string plus a NULL terminator).
    """
    buf = _ffi.new('char *', 33)
    _LIB.SDL_JoystickGetGUIDString(unbox(a0), buf, 33)
    return _ffi.string(buffer)
