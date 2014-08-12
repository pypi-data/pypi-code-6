#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: __INIT__.PY
Date: Friday, November 11 2011
Description: Init module.


Documentation for LSPI

D : tuples of (s,a,r,ns,na)
epsilon : threshold for stopping
env : used to evaluate the action of the current policy on the next state and provides phi(s,a)
policy0: the initial policy
"""

from .lspi import LSPI, LSPIRmax
from .lstdq import LSTDQ, OptLSTDQ, FastLSTDQ, ParallelLSTDQ, LSTDQRmax, ParallelLSTDQRmax
