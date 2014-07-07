#!/usr/bin/env python

# Name:                         misc_utils
#
# Author: Ian Stewart
#
# Contents:
#	fracVal
#	getBinNumber
#	class GetNextCLArg
#	matMul
#	maxloc
#	minloc
#	pack_index_2
#	strToList
#
# TODO:
#	- Implement more tests.
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

"""Description: Contains miscellaneous utility functions."""

_module_name = 'misc_utils'

import sys
#import math
#import pickle
import numpy as nu
#import scipy
#from scipy import special

#import ims_exceptions as ex
import local_exceptions as ex

_defaultPadFrac = 0.05

#.......................................................................
def padBoth(xLo, xHi, padFrac=_defaultPadFrac):
  padSize = (xHi - xLo) * padFrac / (1.0 - 2.0 * padFrac)
  paddedXLo = xLo - padSize
  paddedXHi = xHi + padSize
  return (paddedXLo, paddedXHi)
  
#.......................................................................
def doPadLimits(xLo, xHi, yLo, yHi, padFrac=_defaultPadFrac):
  (paddedXLo, paddedXHi) = padBoth(xLo, xHi, padFrac)
  (paddedYLo, paddedYHi) = padBoth(yLo, yHi, padFrac)
  return (paddedXLo, paddedXHi, paddedYLo, paddedYHi)

#-----------------------------------------------------------------------
def fracVal(lowerLimit, upperLimit, fracBetween0and1):
  # The double subtraction from 1 is to ensure that the multipliers
  # of lowerLimit and upperLimit add exactly to 1. If this were not done, numerical
  # rounding effects can cause the result to be, for example, less than
  # lowerLimit for small positive values of fracBetween0and1.
  value = (1.0 - fracBetween0and1) * lowerLimit + (1.0 - (1.0 - fracBetween0and1)) * upperLimit
  return value

#-----------------------------------------------------------------------
class TooFewEdges(Exception):
  def __init__(self, numEdges):
    self.numEdges = numEdges
  def __str__(self):
    return 'Number of edges is only %d but must be > 1.' % (self.numEdges)

class _XOutOfRange(Exception):
  def __init__(self, x, xEdge):
    self.x = x
    self.xEdge = xEdge
#  def __str__(self):
#    return 'Bin number for this x value is %d' % (self.binNum)

class XTooLow(_XOutOfRange):# pass
  def __str__(self):
    return 'Value %f < the lowest edge %f.' % (self.x, self.xEdge)

class XTooHigh(_XOutOfRange):# pass
  def __str__(self):
    return 'Value %f > the highest edge %f.' % (self.x, self.xEdge)

def _getBinNumberBisect(xBinEdges, x):
  """Ported from subroutine getBinNumberDouble_new_locate in the XMM-Newton SAS module ssclib/array_utils.f90. Ultimately derives from Press et al. ****Rethunk 2010-10-05. IMS."""

  numEdges = len(xBinEdges)

  if numEdges < 2: raise ex.Bug('Need > 1 edge but only %d found.' % (numEdges))
  if x < xBinEdges[0] or x >= xBinEdges[-1]: raise ex.Bug('Value %f out of range [%f, %f].' % (x, xBinEdges[0], xBinEdges[-1]))

  edgeILo = 0
  edgeIHi = numEdges-1
  while (edgeIHi - edgeILo > 1):
    edgeIMid = (edgeILo + edgeIHi) // 2
    if (x >= xBinEdges[edgeIMid]):
      edgeILo = edgeIMid
    else:
      edgeIHi = edgeIMid

  binNum = edgeILo
  return binNum

#-----------------------------------------------------------------------
def getBinNumber(xBinEdges, x, guessedBinNum=None):
  """Ported from the subroutine of that name in the XMM-Newton SAS module ssclib/array_utils.f90. (Ultimately derives from Press et al.)

This function is designed to return the index or number of the bin (the first bin is binNum = 0) in which the input value x falls. The function performs as follows:

It compares the value of x with the bin 'edges' stored in xBinEdges.

If x < xBinEdges[0], an XTooLow error is raised.

If xBinEdges[i] <= x < xBinEdges[i+1], binNum = i is returned.

If xBinEdges[len(xBinEdges)-2] <= x <= xBinEdges[len(xBinEdges)-1], binNum = len(xBinEdges)-2 is returned.

If x > xBinEdges[len(xBinEdges)-1], an XTooHigh error is raised.

****Rethunk 2010-10-05. IMS."""

  _testFlag = False

  numBins = len(xBinEdges)-1
  if numBins < 1: raise TooFewEdges(numBins+1)

#  if _testFlag:
#    print 'In misc_utils.getBinNumber: xBinEdges[0]=', xBinEdges[0]

  if x < xBinEdges[0]:  raise XTooLow( x, xBinEdges[0])
  if x > xBinEdges[-1]: raise XTooHigh(x, xBinEdges[-1])

  # Special case:
  #
  if x==xBinEdges[-1]:
    return numBins-1

  if guessedBinNum==None or guessedBinNum < 0 or guessedBinNum > numBins-1:
    # input guess is not useful, go straight to bisection routine.
    #
    try:
      binNum = _getBinNumberBisect(xBinEdges, x)
    except ex.Bug():
      print 'x, edgeILo, edgeIHi, numBins, xBinEdges[edgeILo], xBinEdges[edgeIHi], xBinEdges[0], xBinEdges[-1]:'
      print  x, edgeILo, edgeIHi, numBins, xBinEdges[edgeILo], xBinEdges[edgeIHi], xBinEdges[0], xBinEdges[-1]
      raise

    if _testFlag and binNum==0:
      print 'In misc_utils.getBinNumber: _getBinNumberBisect has returned binNum=0; x=', x

    return binNum

  stepI = 1
  if x >= xBinEdges[guessedBinNum]: # hunt upward:
    edgeILo = guessedBinNum
    while True: # double size of step at each iteration.
      edgeIHi = edgeILo + stepI

      if edgeIHi > numBins: # done hunting, because off end of table; set up for bisection.
        edgeIHi = numBins
        break

      if x < xBinEdges[edgeIHi]: # done hunting, value bracketed; set up for bisection.
        break

      # If got to here, not done hunting, and x is still >= xBinEdges[edgeIHi].

      edgeILo = edgeIHi
      stepI = stepI + stepI
    # end of step-doubling loop.

  else: # x < xBinEdges[guessedBinNum]: hunt downward:
    edgeIHi = guessedBinNum
    while True: # double size of step at each iteration.
      edgeILo = edgeIHi - stepI

      if (edgeILo < 0): # done hunting, because off end of table; set up for bisection.
        edgeILo = 0
        break

      if (x >= xBinEdges[edgeILo]): # done hunting, value bracketed; set up for bisection.
        break

      # If got to here, not done hunting, and x is still < xBinEdges[edgeILo].

      edgeIHi = edgeILo
      stepI = stepI + stepI
    # end of step-doubling loop.
  # end decide hunt up or down.

  # If we have reached here, then x is guaranteed to be >= xBinEdges[edgeILo] and < xBinEdges[edgeIHi]. Send the slice of xBinEdges to the bisection search:
  #
  try:
    binNum = edgeILo + _getBinNumberBisect(xBinEdges[edgeILo:edgeIHi+1], x)
  except ex.Bug():
    print 'x, edgeILo, edgeIHi, numBins, xBinEdges[edgeILo], xBinEdges[edgeIHi], xBinEdges[0], xBinEdges[-1]:'
    print  x, edgeILo, edgeIHi, numBins, xBinEdges[edgeILo], xBinEdges[edgeIHi], xBinEdges[0], xBinEdges[-1]
    raise

  return binNum

#-----------------------------------------------------------------------
class GetNextCLArg:
  def __init__(self, printIndex=False):
    self.printIndex = printIndex
    self.csi = 1

  def __call__(self, dataType='str'):
    nextArgStr = sys.argv[self.csi]
    if self.printIndex: print 'Reading command line argument %d: %s' % (self.csi, nextArgStr)
    self.csi += 1

    if   dataType=='str':
      if nextArgStr=='None':
        nextArg = None
      else:
        nextArg = nextArgStr

    elif dataType=='float':
      if nextArgStr=='None':
        nextArg = None
      else:
        nextArg = float(nextArgStr)

    elif dataType=='int':
      if nextArgStr=='None':
        nextArg = None
      else:
        nextArg = int(nextArgStr)

    elif dataType=='bool':
      nextArg = strToBool(nextArgStr)

    else:
      raise ex.UnrecognizedChoiceObject(dataType)

    return nextArg

#-----------------------------------------------------------------------
class BadShape(ex.Report): pass
#  def __init__(self, message):
#    self.message = message
#  def __str__(self)

def matMul(mat1, mat2):
  """implements a matrix multiplication, which seems to be absent from numpy. If we write Rn, Cn for the number of rows and columns respectively of matrix n, then C1 must = R2."""

  numDimsMat1 = len(mat1.shape)
  numDimsMat2 = len(mat2.shape)

  if not (numDimsMat1==1 or numDimsMat1==2):
    raise 'bad shape array 1'
  if not (numDimsMat1==2 or numDimsMat2==2):
    raise 'bad shape array 2'

  if numDimsMat1==1:
    if numDimsMat2==1:
      outMat = (mat1 * mat2).sum()
    else: # numDimsMat2==2
      tempMat1 = mat1.reshape(1,mat1.shape[0])
      outMat = _matMul2x2(tempMat1, mat2).squeeze()
  else: # numDimsMat1==2
    if numDimsMat2==1:
      tempMat2 = mat2.reshape(mat2.shape[0],1)
      outMat = _matMul2x2(mat1, tempMat2).squeeze()
    else: # numDimsMat2==2
      outMat = _matMul2x2(mat1, mat2)

  return outMat

def _matMul2x2(mat1, mat2):
  [r1, c1] = mat1.shape
  [r2, c2] = mat2.shape

  dataTypeTester = nu.array([mat1[0,0]*mat2[0,0]])
  outMat = nu.zeros([r1, c2],dataTypeTester.dtype)

  for row in range(r1):
    for col in range(c2):
      outMat[row,col] = (mat1[row,:]*mat2[:,col]).sum()

  return outMat

#-----------------------------------------------------------------------
def maxloc(arr):
  """Returns indices of the maximum-value element of the input array."""
  i = nu.ma.argmax(nu.ma.ravel(arr)) # caters for masked as well as ordinary arrays.

  try:
    vectorOfIndices = pack_index_2(arr.shape,i)
    return vectorOfIndices
  except AttributeError: # assume arr is a simple list.
    return i

#-----------------------------------------------------------------------
def minloc(arr):
  """Returns indices of the minimum-value element of the input array."""
  i = nu.ma.argmin(nu.ma.ravel(arr)) # caters for masked as well as ordinary arrays.

  try:
    vectorOfIndices = pack_index_2(arr.shape,i)
    return vectorOfIndices
  except AttributeError: # assume arr is a simple list.
    return i

#.......................................................................
def pack_index_2(shape, i):
  # This is the function which was previously located in plot_utils_1 and named wrap_index. There are no comments in the other function but I think it does the same as pack_index. Some time I ought to compare the two pack_indexes and see which is better. It is notable that _2 is so much shorter and neater. IMS 2009-11-06.

  indices = [-1]*len(shape)
  for k in range(len(shape)-1,0,-1):
    dimm = shape[k]
    indices[k] = i%dimm
    i = i // dimm
  indices[0] = i
  return indices

#-----------------------------------------------------------------------
def strToBool(inStr):
  """This takes any reasonable synonym for 'true/false' and converts it to the appropriate boolean. The default is False."""

  lcStr = inStr.lower()
  if lcStr=='true' or lcStr=='t' or lcStr=='yes' or lcStr=='1':
    outBool = True
  else:
    outBool = False

  return outBool

#-----------------------------------------------------------------------
def strToFloat(myStr):
  if myStr=='None':
    return None
  else:
    return float(myStr)

#-----------------------------------------------------------------------
def strToInt(myStr):
  if myStr=='None':
    return None
  else:
    return int(myStr)

#-----------------------------------------------------------------------
def strToList(myListStr, dataType='str'):
  strsList = myListStr.split()
  argList = []
  for myStr in strsList:
    if dataType=='bool':
      arg=strToBool(myStr)
    elif dataType=='float':
      arg=strToFloat(myStr)
    elif dataType=='int':
      arg=strToInt(myStr)
    else:
      arg=myStr

    argList.append(arg)

  return argList


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  pass
