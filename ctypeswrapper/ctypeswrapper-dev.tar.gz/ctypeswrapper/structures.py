import ctypes
import itertools


class Enum(dict):
    def __init__(self, name, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.reverse = dict([(self[n], n) for n in self])
        self.name = name

    def name_to_value(self, name):
        return dict.__getitem__(self, name)

    def value_to_name(self, value):
        return self.reverse[value]

    def __getitem__(self, k):
        if isinstance(k, (str, unicode)):
            return self.name_to_value(k)
        elif isinstance(k, int):
            return self.value_to_name(k)
        else:
            raise ValueError(
                "Invalid enum key {}, must be str, unicode or int: {}".format(
                    k, type(k)))


def arg_type_convert(v, atype=None, ptype=None, byref=None):
    """
    This needs to know the un-pointered type when arg by value
    """
    if byref:
        if type(v) == atype:
            return v
        # this should be a simple ctype that will be pointed to
        if type(v).__module__ == 'ctypes':  # this is a valid ctypes object
            return ctypes.byref(v)
        if type(type(v)).__module__ == '_ctypes':  # defined struct, etc
            return ctypes.byref(v)
        # this is a non-ctypes object, so making it into a ctypes object
        # would 'shadow' the arg, causing any change to the generated
        # ctype object to be lost. so throw an exception
        raise Exception(
            "Arguments passed by reference must "
            "be ctypes object: {}, {}".format(v, type(v)))
    if type(v) != atype:
        return atype(v)
    return v


class Function(object):
    def __init__(self, name, restype, *args):
        self.name = name
        self.restype = restype
        self.args = args
        self.func = None
        self.lib = None
        self.converter = None

    def as_ctype(self):
        return ctypes.CFUNCTYPE(self.restype, *[a[1] for a in self.args])

    def generate_spec(self, lib):
        # TODO do I need the namespace here... probably for typedefs
        self.converter = []
        # TODO generate converter for __call__, maybe even a *gasp* doc string
        for n, vt in self.args:
            argtype = type(vt).__name__  # this is a type of a type
            if argtype == 'PyCSimpleType':  # pass by value
                self.converter.append(
                    lambda v, a=vt, b=False:
                    arg_type_convert(v, a, b)
                    )
            elif argtype == 'PyCPointerType':  # pass by ref
                self.converter.append(
                    lambda v, a=vt, b=True:
                    arg_type_convert(v, a, b)
                    )
            elif argtype == 'PyCStructType':
                self.converter.append(
                    lambda v, a=vt, b=False:
                    arg_type_convert(v, a, b)
                    )
            else:
                raise Exception(
                    "Unknown arg type {} for {} {}".format(argtype, n, vt))
        self.assign_lib(lib)
        self.__doc__ = 'args: {}'.format(self.args)

    def assign_lib(self, lib):
        self.lib = lib
        self.func = getattr(self.lib, self.name)
        self.func.restype = self.restype
        self.func.argtypes = [v for _, v in self.args]

    def __call__(self, *args):
        if self.func is None:
            raise Exception(
                "Function has not been bound to a library: see assign_lib")
        if self.converter is None:
            raise Exception(
                "Function spec has not been generated: see generate_spec")
        if len(self.converter) != len(args):
            raise Exception(
                "Invalid number of args {} != {}".format(
                    len(args), len(self.converter)))
        return self.func(*[
            c(a) for (c, a) in itertools.izip(self.converter, args)])
