# Base class for struct helpers.

import sys

from .dso import ffi, _LIB

class Struct(object):
    """
    Wrap a cffi structure in a Python class, hiding allocation and
    dereferencing.
    """
    def __init__(self, data=None, ffi=ffi):
        if isinstance(data, ffi.CData):
            self.cdata = data
        elif isinstance(data, Struct):
            self.cdata = data.cdata
        else:
            self.cdata = ffi.new("%s *" % (self.__class__.__name__), data)

    def __nonzero__(self):
        return bool(self.cdata)

def unbox(data, c_type=None, ffi=ffi, nullable=False):
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
            if data is None and nullable:
                return ffi.NULL
            if c_type:
                return ffi.new(c_type, data)
    return data

class SDLError(Exception):
    """Fetch and wrap the current SDL error message."""
    def __init__(self):
        message = ffi.string(_LIB.SDL_GetError()).decode('utf-8')
        assert message, 'SDL reports no error.' # don't call us when there is no error!
        Exception.__init__(self, message)

if sys.version_info[0] == 2:
    def u8(text):
        """Automatically encode text to UTF-8."""
        if isinstance(text, unicode):
            return text.encode('utf-8')
        return text
else:
    def u8(text):
        """Automatically encode text to UTF-8."""
        return text.encode('utf-8')
