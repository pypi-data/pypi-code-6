#!/usr/bin/env python

import ctypes

from . import namespace
from . import parser


def wrap(header_filename, library_filename):
    lib = ctypes.cdll.LoadLibrary(library_filename)
    rep = parser.parse_filename(
        header_filename, use_cpp=True, fake_stdlib=True)
    return namespace.NameSpace(lib, rep)
