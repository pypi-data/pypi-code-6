#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# IAPWS for seawater
###############################################################################

from __future__ import division
from math import log, exp, tan, atan, acos, sin

from iapws95 import IAPWS95
from _iapws import _Ice


if __name__ == "__main__":
    import doctest
    doctest.testmod()
