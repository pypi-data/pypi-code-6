#!/usr/bin/env python
"""
Take a parsed representation (from parser.parse)
and generate ctypes bindings
"""


class NameSpace(object):
    def __init__(self, lib, rep):
        self._lib = lib
        self._generate(lib, rep)

    def _generate(self, lib, rep):
        for (n, v) in rep:
            vt = type(v).__name__
            # TODO this can probably be simplified
            if vt == 'PyCStructType':
                # struct
                setattr(self, n, v)
            elif vt == 'Function':
                # function
                v.generate_spec(lib)
                setattr(self, n, v)
            elif vt == 'Enum':
                setattr(self, n, v)
            elif vt == 'PyCPointerType':
                # pointer to something?? TODO
                setattr(self, n, v)
            elif vt == 'PyCSimpleType':
                setattr(self, n, v)
            else:
                raise Exception(
                    "Unknown representation value type {}".format(vt))
