#!/usr/bin/env python

# Name:                         transforms
#
# Author: Ian Stewart
#
# Contents:
#	class _Transform:
#
# TODO:
#
#    vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#    Copyright (C) 2014  Ian M Stewart
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    For the GNU General Public License, see <http://www.gnu.org/licenses/>.
#    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# History (date, change author):
#
#	2014-05-09	IMS/AIfA
#.......................................................................
# + First draft. Code extracted and modified from parameter.py.
#
#	2014-05-14	IMS/AIfA
#.......................................................................
# * Copied to this release version.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
Class definitions for objects which transform coordinates in various ways.
"""

_module_name = 'transforms'

import math

#import ims_exceptions as ex
import local_exceptions as ex
#import SciMathConstants as const

_lnTen = math.log(10.0)

#.......................................................................
class _Transform:
  """
This defines a parameter transformation q = f(p).
  """
  codeStr = ''
  numSetupArguments = None

#  def __init__(self, listOfSetupArgs=[]):
#    raise ex.EmptyMethod()

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    raise ex.EmptyMethod()
    return qValue

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    raise ex.EmptyMethod()
    return pValue

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
    raise ex.EmptyMethod()
    return dqOnDp

#.......................................................................
class TransformChain:
  """
This defines a parameter transformation q = f(p).
  """
  codeStr = 'chain'
  numSetupArguments = None

  def __init__(self, listOfTransforms=[]):
    self.listOfTransforms = listOfTransforms

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    qValue = pValue
    for transform in self.listOfTransforms:
      qValue = transform.transform(qValue)

    return qValue

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    pValue = qValue
    for transform in self.listOfTransforms:
      pValue = transform.deTransform(pValue)

    return pValue

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
    dqOnDp = 1.0
    qValue = pValue
    for transform in self.listOfTransforms:
      dqOnDp *= transform.calcDeriv(qValue)
      qValue  = transform.transform(qValue) # last one is unnecessary.

    return dqOnDp

#.......................................................................
class TransformIdentity(_Transform):
  """
This defines a parameter transformation q = f(p) where f() is the identity operation.
  """
  codeStr = None
  numSetupArguments = 0 # max is 10.

#  def __init__(self):
#    pass

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    return pValue

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    return qValue

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
    return 1.0 # argument 'pValue' is not used

#.......................................................................
class TransformLinear(_Transform):
  """
This defines a parameter transformation q = f(p) where f(p) = a + b*p.
  """
  codeStr = 'linear'
  numSetupArguments = 2 # max is 10.

  def __init__(self, listOfSetupArgs):
    [self.intercept, self.slope] = listOfSetupArgs

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    return self.intercept + self.slope * parValue

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    return (qValue - self.intercept) / self.slope

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
    return self.slope # argument 'pValue' is not used

#.......................................................................
class TransformLn(_Transform):
  codeStr = 'ln'
  numSetupArguments = 0 # max is 10.

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    return math.log(pValue)

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    return math.exp(pValue)

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
    return 1.0 / pValue

#.......................................................................
class TransformLog10(_Transform):
  codeStr = 'log10'
  numSetupArguments = 0 # max is 10.

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    return math.log10(pValue)

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    return 10.0**(qValue)

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
#    return 1.0 / const.lnTen / pValue
    return 1.0 / _lnTen / pValue

#.......................................................................
class TransformDecircle(_Transform):
  """
This defines a parameter transformation q = 1/sqrt(1-u^2) where u = .... mucked this up somehow.
  """
  codeStr = 'decircle'
  numSetupArguments = 2 # max is 10.

  def __init__(self, lo, hi):
    raise 'this transform needs work.'
    self.lo = lo
    self.hi = hi
    self.delta = hi - lo
#    self.addnlInfos = [lo,hi]

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    u = 2.0*(pValue - self.lo)/self.delta - 1.0
    q = 1.0/math.sqrt(1.0-u*u)
    return q

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    u = cmp(qValue,0.0)\
      * math.sqrt(1.0 - 1.0/qValue/qValue) # the cmp(,0) is equivalent to sign().
    p = self.lo + self.delta * (u + 1.0) / 2.0
    return p

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
    u = 2.0*(pValue - self.lo)/self.delta - 1.0
    dqOnDp = 2.0 * u / self.delta / (1.0 - u*u)**1.5
    return dqOnDp

#.......................................................................
class TransformTan(_Transform):
  """
This defines a parameter transformation

	       (      [ p - lo  ]       )
	q = tan( pi * [---------] - pi/2)
	       (      [ hi - lo ]       )
  """
  codeStr = 'tan'
  numSetupArguments = 2 # max is 10.

  def __init__(self, listOfSetupArgs):
    [self.lo, self.hi] = listOfSetupArgs
    self.delta = hi - lo
#    self.addnlInfos = [lo, hi]

  def transform(self, pValue):
    """
Given p, this returns q = f(p).
    """
    u = math.pi*((pValue - self.lo)/self.delta - 0.5)
    q = math.tan(u)
    return q

  def deTransform(self, qValue):
    """
Given q, this returns p = f^{-1}(q).
    """
    u = math.atan(qValue)
    p = ((u / math.pi) + 0.5) * self.delta + self.lo
    return p

  def calcDeriv(self, pValue):
    """
              dq |
This returns ----|
              dp |p=p
    """
    q = self.transform(pValue)
    dqOnDp = (1.0 + q*q) * math.pi / self.delta
    return dqOnDp

#.......................................................................
def transformChooser(transformIdStr, addnlInfos=[]):
#  print transformIdStr
  if transformIdStr=='log10':
    return TransformLog10()
  elif transformIdStr=='ln':
    return TransformLn()
  elif transformIdStr=='tan':
    return TransformTan(addnlInfos)
  else:
    raise ex.UnrecognizedChoiceObject(transformIdStr)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__=='__main__':

  pass




























