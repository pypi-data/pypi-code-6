# -*- coding: utf-8 -*-


import sys


if sys.version_info[0] == 2:
    from .py2 import raise_, raise_from
else:
    from .py3 import raise_, raise_from


def reraise():
    """
    Does the same that ``raise`` without arguments do in Python2.
    But in both Python 2 and Python 3 (>= 3.3).
    """
    raise_(*sys.exc_info())


# silence pyflakes
assert reraise
assert raise_
assert raise_from
