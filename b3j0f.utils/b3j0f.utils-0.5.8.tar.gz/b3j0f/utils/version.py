# -*- coding: utf-8 -*-

"""
Module which provides variables and constants in order to ease developments
among several python versions and platforms.
"""

from __future__ import unicode_literals

from sys import version_info
from platform import python_implementation

PY3 = version_info[0] == 3  #: python3
PY2 = version_info[0] == 2  #: python2
PY26 = PY2 and version_info[1] == 6  #: python2.6
PYPY = python_implementation() == 'PyPy'  #: pypy
CPYTHON = python_implementation() == 'CPython'  #: cpython
JYTHON = python_implementation() == 'Jython'  #: jython
IRONPYTHON = python_implementation() == 'IronPython'  #: IronPython

if PY3:
    basestring = str
else:
    basestring = str, unicode
