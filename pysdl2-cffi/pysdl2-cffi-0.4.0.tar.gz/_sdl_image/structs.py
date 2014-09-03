# Base class for struct helpers.

import _sdl.structs
from .dso import ffi

class Struct(_sdl.structs.Struct):
    """
    Wrap a cffi structure in a Python class, hiding allocation and
    dereferencing.
    """
    def __init__(self, cdata=ffi.NULL, ffi=ffi):
        _sdl.structs.Struct.__init__(self, cdata, ffi)

def unbox(data, c_type=None, ffi=ffi):
    """
    Try to return something to pass to low-level ffi calls.
    For a cffi type, return data.
    For a Struct, return the wrapper's cdata.
    Else try to use data as a ffi initializer for c_type.
    """
    if not isinstance(data, ffi.CData):
        try:
            return data.cdata
        except AttributeError:
            if c_type:
                return ffi.new(c_type, data)
    return data
