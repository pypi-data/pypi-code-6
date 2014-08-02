#!/usr/bin/env python
import struct

class Buffer(object):
    pass

class Protocol(object):

    def __init__(self):
        self._values = ''
        self._names = []
    
    def add_type(self, name, dtype, mult):
        self._values += str(mult) + dtype
        self._names += [(name, dtype, mult)]

    def add_byte(self, name, signed=False, mult=1):
        if signed:
            dtype = 'b'
        else:
            dtype = 'B'
        self.add_type(name, dtype, mult)

    def add_half(self, name, signed=True, mult=1):
        if signed:
            dtype = 'h'
        else:
            dtype = 'H'
        self.add_type(name, dtype, mult)

    def add_int(self, name, signed=True, mult=1):
        if signed:
            dtype = 'i'
        else:
            dtype = 'I'
        self.add_type(name, dtype, mult)

    def add_long(self, name, signed=True, mult=1):
        if signed:
            dtype = 'l'
        else:
            dtype = 'L'
        self.add_type(name, dtype, mult)

    def add_quad(self, name, signed=True, mult=1):
        if signed:
            dtype = 'q'
        else:
            dtype = 'Q'
        self.add_type(name, dtype, mult)

    def add_float(self, name, mult=1):
        self.add_type(name, 'f', mult)

    def add_double(self, name, mult=1):
        self.add_type(name, 'd', mult)

    def add_num(self, name, size=4, signed=True, mult=1):
        if size == 1:
            self.add_byte(name, signed=signed, mult=mult)
        elif size == 2:
            self.add_half(name, signed=signed, mult=mult)
        elif size == 4:
            self.add_int(name, signed=signed, mult=mult)
        if size == 8:
            self.add_quad(name, signed=signed, mult=mult)
    
    def add_str(self, name, size=1):
        if size == 'v':
            dtype = 'p'
            size = ''
        else:
            dtype = 's'
        self.add_type(name, dtype, size)

    def create(self, values, order='<'):
        unpacked = struct.unpack(order + self._values, values)
        buf = Buffer()
        i = 0
        for name, dtype, mult in self._names:
            if dtype not in ('s', 'p') and mult > 1:
                vals = unpacked[i:i+mult]
                setattr(buf, name, vals)
                i += mult
            else:
                setattr(buf, name, unpacked[i])
                i += 1
        return buf
