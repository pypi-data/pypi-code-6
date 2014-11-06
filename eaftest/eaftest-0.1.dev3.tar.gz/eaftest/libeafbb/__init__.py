#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import ctypes
from ctypes import c_int
import ctypes.util
import numpy as np
c_int_arr = np.ctypeslib.ndpointer(dtype=np.int32)

LIB_PATH = os.path.join(os.path.dirname(__file__), "libeafbb.so")
_lib = ctypes.cdll.LoadLibrary(LIB_PATH)

_lib.init_from_arrays.argtypes = [c_int_arr, c_int_arr, c_int, c_int, c_int]
_lib.init_from_arrays.restype = None
_lib.set_debug_level.argtypes = [c_int]
_lib.set_debug_level.restype = None
_lib.run_test_mask.argtypes = [c_int]
_lib.run_test_mask.restype = c_int


def test_mask(maskn):
    return _lib.run_test_mask(maskn)

def init(points, masks):
    nvars, npoints, nmasks = len(points[0]), len(points), len(masks)
    return _lib.init_from_arrays(points, masks, nvars, nmasks, npoints)

def set_debug(level=2):
    _lib.set_debug_level(level)

def runkernel(points, masks):
    nmasks = len(masks)
    
    # FIXME: Possivelmente redundante
    points = np.array(points, dtype=np.int32)
    masks  = np.array(masks, dtype=np.int32)

    set_debug()
    init(points, masks)

    set_debug(0)
    for i in range(nmasks):
        yield test_mask(i)


