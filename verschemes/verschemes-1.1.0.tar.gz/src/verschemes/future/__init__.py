# -*- coding: utf-8 -*-
"""verschemes.future module

This is equivalent to future.builtins with customizations.

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from future.builtins import *
from future.builtins import __all__ as _all
from future import utils as future


_all = set(_all)

if future.PY2:
    _all |= set(['str', 'super', 'type'])
    from verschemes.future.newstr import newstr as str
    from verschemes.future.newsuper import newsuper as super
    from verschemes.future.newtype import newtype as type

_all.add('future')
__all__ = list(future.native_str(x) for x in _all)
