#!/usr/bin/env python

# Name:                         math_utils
#
# Author: Ian Stewart
#
# Contents:
#	finiteDifference
#	integralOfGaussian
#	transformCovarMat
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
#	2014-05-14	IMS/AIfA
#.......................................................................
# * Copied to this release version. Only a few functions retained.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_module_name = 'math_utils'

import sys
import math
import numpy as nu
from scipy import special

#import SciMathConstants as const
import misc_utils as mu

_twoPi = 2.0 * math.pi
#precision = abs(0.1-((1.0+0.1)-1.0))
precision = sys.float_info.epsilon
epsilon = precision
exponentPrecision = -math.log10(precision)
tiny = sys.float_info.min
huge = sys.float_info.max
#_sincMinArg = math.sqrt(2.0)*(precision * 120.0)**0.25
qTiny = 1.0e-30 ### kind of arbitrary.
_expLarge = 100.0 # arbitrary

_rootPi = math.sqrt(math.pi)
_rootTwo = math.sqrt(2.0)

_testFlag = False

#-----------------------------------------------------------------------
def binomialCoefficients(n):
  """Returns

	    (n)       n!
	W = ( ) = ----------
	    (k)    k!(n-k)!

for each k in {0...n}. The calculation is via the recurrence relation which walks along the nth row of Pascal's Triangle. This is slow but returns an integer value.
  """

  pascalsTriangle = nu.ones([n+1,n+1], nu.int)
  for row in range(2,n+1):
    for col in range(1,row):
      pascalsTriangle[row,col] = pascalsTriangle[row-1,col-1] + pascalsTriangle[row-1,col]

  return pascalsTriangle[n,:]

#-----------------------------------------------------------------------
def fdTestFunction(r):
  x = r[0]
  y = r[1]
  
  func = 3.5 + 2.0*x*x - 1.7*x*y*y - 2.7*y + 0.3*y*y*y
  return func

def finiteDifference(f, r0, deltaList):
  """This function is designed to return the finite difference approximation of a derivative to any order, in any combination of axes, of the function of a vector argument supplied as 'f'. The arguments to the present function are described as follows:

	f This should be an object which can be treated like a function, taking as its sole argument a numpy vector of floats r_, and returning a scalar float. This is the function of which the derivatives are found.
  
	r0  The reference value of r_ at which the derivatives are calculated.
  
	deltaList is a list, each element of which is a dictionary with the structure
		{'index':int, 'delta':float}
	'index' is the axis (i.e., the relevant index of r_) and 'delta' is the distance along that axis between the two samples at which f() will be evaluated to calculate the FD.

The routine works iteratively. At each level, the last element of deltaList is popped from the list and a FD approximation of the 1st derivative of f() with respect to the axis given by 'index' of the popped value and with distance between the samples on that axis given by 'delta' of the popped value. If there are remaining elements to deltaList, the function evaluated is a further call to finiteDifference() with r0[index] offset by + or - delta/2 as appropriate, and the truncated deltaList supplied. If on the other hand deltaList has been exhausted by the current pop, f() is evaluated at r_ = r0 with r0[index] offset by + or - delta/2.
  """

  _tf=False
  if _tf: print '>>>>> Entering finiteDifference().'

  localList = deltaList[:] # otherwise it modifies the argument as a side effect!
  lastElement = localList.pop()
  i  = lastElement['index']
  dx = lastElement['delta']
  
  rPos = r0.copy()
  rPos[i] += dx/2.0
  rNeg = r0.copy()
  rNeg[i] -= dx/2.0

  if _tf:
    print 'rPos:\n', rPos
    print 'rNeg:\n', rNeg

  if len(localList)<1:
    if _testFlag:
      print ''
      print 'math_utils.finiteDifference(), about to calc yNeg for index %d' % (i)
    yNeg = f(rNeg)
    if _testFlag:
      print ''
      print 'math_utils.finiteDifference(), about to calc yPos for index %d' % (i)
    yPos = f(rPos)
    if _tf:
      print 'yPos, yNeg:', yPos, yNeg

  else:
    if _testFlag:
      print ''
      print 'math_utils.finiteDifference(), about to calc yNeg for index %d' % (i)
    yNeg = finiteDifference(f, rNeg, localList)
    if _testFlag:
      print ''
      print 'math_utils.finiteDifference(), about to calc yPos for index %d' % (i)
    yPos = finiteDifference(f, rPos, localList)
  
  result = (yPos - yNeg) / dx
  if _tf: print '<<<<< Leaving finiteDifference().'
  return result

#-----------------------------------------------------------------------
def integralOfGaussian(sigma, x0=0.0, xLo=None, xHi=None):
  """This is just a handy short cut to the erf function of correct argument. Note this is for the integral of an UNNORMALIZED gaussian.

Note that a value of 'None' means that bound is infinite."""

#  premultiplier = sigma * const.rootPi / const.rootTwo
  premultiplier = sigma * _rootPi / _rootTwo

  if xLo==None and xHi==None:
    return premultiplier * 2.0

  if xLo==None:
    if xHi >= x0:
#      return premultiplier * (1.0 + special.erf((xHi-x0) / sigma / const.rootTwo))
      return premultiplier * (1.0 + special.erf((xHi-x0) / sigma / _rootTwo))
    else:
#      return premultiplier * special.erfc(-(xHi-x0) / sigma / const.rootTwo)
      return premultiplier * special.erfc(-(xHi-x0) / sigma / _rootTwo)

  if xHi==None:
    if xLo >= x0:
#      return premultiplier * special.erfc((xLo-x0) / sigma / const.rootTwo)
      return premultiplier * special.erfc((xLo-x0) / sigma / _rootTwo)
    else:
#      return premultiplier * (1.0 + special.erf(-(xLo-x0) / sigma / const.rootTwo))
      return premultiplier * (1.0 + special.erf(-(xLo-x0) / sigma / _rootTwo))

#  return premultiplier * (special.erf((xHi-x0) / sigma / const.rootTwo) - special.erf((xLo-x0) / sigma / const.rootTwo))
  return premultiplier * (special.erf((xHi-x0) / sigma / _rootTwo) - special.erf((xLo-x0) / sigma / _rootTwo))

#-----------------------------------------------------------------------
def transformCovarMat(matrixOfDerivs, oldCovarMatrix):
  """
Suppose we have a function F which is defined in terms of parameters p_ = [p_1, p_2, ... p_M]. Let the covariance between these parameters be expressed via the MxM matrix C_old. If we reparameterize F in terms of parameters q_ = [q_1, q_2, ... q_N] such that

	q_ = D * p_,

then the new covariance matrix is given by

	C_new = D * C_old * D^T.

Here the 'T' superscript indicates transpose. Both input arguments should be 2D numpy array objects.

Proof:

	C_new = E[q_*q_^T]
	    = E[D*p_*p_^T*D^T]
	    = D*E[p_*p_^T]*D^T
	    = D * C_old * D^T.

See also

	http://www.cs.bc.edu/~alvarez/Randomness/Notes/covAfterLinear
"""

  return mu.matMul(matrixOfDerivs, mu.matMul(oldCovarMatrix, matrixOfDerivs.transpose()))


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  pass

