# -*- coding: utf-8 -*-
"""
A place for different utilities.
"""
import sys


if sys.version_info[0] == 3:  # pragma: no cover
    text_type = str
else:  # pragma: no cover
    text_type = unicode
