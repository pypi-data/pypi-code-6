# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------
# xoutil.cpycode
#----------------------------------------------------------------------
# Copyright (c) 2014 Merchise Autrement and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2014-04-18

"""Byte-code utilities for CPython.

This module facilitates working at the byte-code level.  This module breaks
the expectation of working the same in Python 2.7 and Python 3.0+, since it's
too low-level and the byte-code has changed somehow within this span of
versions.

"""

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        unicode_literals as _py3_unicode,
                        absolute_import as _py3_abs_import)


def assemble(instructions):
    """Assemble byte-code instructions.

    :param instructions: A list of pairs of ``(byte-code[, arg])``.  The
       `byte-code` is the string that's key in the dictionary
       :obj:`dis.opmap`, and the `arg` is the argument for that instruction.
       If the instruction requires an argument it's an error not to provide
       one.

    :returns: The byte-code string.

    """
    import dis
    import opcode
    import array
    from xoutil import Unset
    result = array.array(str('B'), [])
    for instruction in instructions:
        if len(instruction) > 1:
            opname, oparg = instruction[:2]
        else:
            opname = instruction[0]
            oparg = Unset
        opname = opname.upper()
        opc = opcode.opmap[opname]
        result.append(opc)
        if opc >= dis.HAVE_ARGUMENT:
            if oparg is Unset:
                raise TypeError("'%s' byte-code requires an argument" % opname)
            hi = (oparg & 65280) >> 8
            lo = oparg & 255
            result.extend([lo, hi])
    return result.tostring()
