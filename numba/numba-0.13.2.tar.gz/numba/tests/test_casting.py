import unittest
from numba.compiler import compile_isolated
from numba import types
import struct


def float_to_int(x):
    return types.int32(x)


def int_to_float(x):
    return types.float64(x) / 2


def float_to_unsigned(x):
    return types.uint32(x)

def float_to_complex(x):
    return types.complex128(x)


class TestCasting(unittest.TestCase):
    def test_float_to_int(self):
        pyfunc = float_to_int
        cr = compile_isolated(pyfunc, [types.float32])
        cfunc = cr.entry_point

        self.assertEqual(cr.signature.return_type, types.int32)
        self.assertEqual(cfunc(12.3), pyfunc(12.3))
        self.assertEqual(cfunc(12.3), int(12.3))

    def test_int_to_float(self):
        pyfunc = int_to_float
        cr = compile_isolated(pyfunc, [types.int64])
        cfunc = cr.entry_point

        self.assertEqual(cr.signature.return_type, types.float64)
        self.assertEqual(cfunc(321), pyfunc(321))
        self.assertEqual(cfunc(321), 321./2)

    def test_float_to_unsigned(self):
        pyfunc = float_to_unsigned
        cr = compile_isolated(pyfunc, [types.float32])
        cfunc = cr.entry_point

        self.assertEqual(cr.signature.return_type, types.uint32)
        self.assertEqual(cfunc(-3.21), pyfunc(-3.21))
        self.assertEqual(cfunc(-3.21), struct.unpack('I', struct.pack('i',
                                                                      -3))[0])

    def test_float_to_complex(self):
        pyfunc = float_to_complex
        cr = compile_isolated(pyfunc, [types.float64])
        cfunc = cr.entry_point
        self.assertEqual(cr.signature.return_type, types.complex128)
        self.assertEqual(cfunc(-3.21), pyfunc(-3.21))
        self.assertEqual(cfunc(-3.21), -3.21 + 0j)


if __name__ == '__main__':
    unittest.main()
