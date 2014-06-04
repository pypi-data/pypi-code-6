# Base class for struct helpers.

from .dso import ffi

class Struct(object):
    """
    Wrap a cffi structure in a Python class, hiding allocation and
    dereferencing.
    """
    def __init__(self, data=None, ffi=ffi):
        if not isinstance(data, ffi.CData):
            self.cdata = ffi.new("%s *" % (self.__class__.__name__), data)
	else:
            self.cdata = data

    def __getattr__(self, attr):
        # XXX and if the attribute's value is another struct, return its wrapper
        return getattr(self.cdata[0], attr)

    def __setattr__(self, attr, value):
        if attr == 'cdata':
            super(Struct, self).__setattr__(attr, value)
        else:
            setattr(self.cdata[0], attr, value)

    def __nonzero__(self):
        return bool(self.cdata)

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
