# -*- coding: utf-8 -*-
"""verschemes._types module"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from verschemes.future import *


__all__ = []


__all__.append('int_empty_zero')
class int_empty_zero(int):

    """Subclass of `int` that defaults to zero.

    If the `x` argument is `False`-equivalent, it is transformed to 0, even if
    it is not compatible/parsable by `int`.

    """

    def __new__(cls, *args, **kwargs):
        if args:
            if not args[0]:
                args = list(args)
                args[0] = 0
        elif 'x' in kwargs and not kwargs['x']:
            kwargs['x'] = 0
        return super().__new__(cls, *args, **kwargs)
