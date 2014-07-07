#!/usr/bin/env python

# Name:                         parameter
#
# Author: Ian Stewart
#
# Contents:
#	class ParSpecifications:
#	class ParameterList:
#
# TODO:
#	- should try to modify ParameterList._createFITS_HDUs(self) so it writes nulls for non-relevant prior fields.
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
# * Copied to this release version.
# - Deleted ParameterList, readParsFromFITS and testbed.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""Class definition for a list of model parameters."""

_module_name = 'parameter'

#import os
#import math
import numpy as nu
#import pyfits as pf

#import ims_exceptions as ex
#import misc_utils as mu
#import SciMathConstants as const
import math_utils as ma
import transforms as trn
import priors
#import pyfits_utils as fut

#.......................................................................
class ParSpecifications:
  _tf=False
  def __init__(self, parNames, parUnits=None, parIsPinned=None, priorsObject=None\
    , transformIDs=None, extraTransformsList=[]):
    """
Data types of the arguments:

	- parNames: a list of strings.
	- parUnits: if not at default, a list of strings.
	- parIsPinned: if not at default, a 1D numpy array of booleans.
	- priorsObject: if not at default, an object of class _LnPriors.
	- transformIDs: if not at default, a 1D numpy array of ints.
	- extraTransformsList: a list of _Transform objects.

Note that all the lists/vectors except extraTransformsList should have the same number of elements (if not left at default).
    """
    self.parNames    = parNames
    self.numPars = len(parNames)

    if parUnits==None:
      self.parUnits = ['']*self.numPars
    else:
      self.parUnits    = parUnits

    if parIsPinned==None:
      self.parIsPinned = nu.zeros([self.numPars],nu.bool)
    else:
      self.parIsPinned = parIsPinned

    if priorsObject==None:
      self.priors = priors.LnPriorsFlat()
    else:
      self.priors = priorsObject


    self.numUnpinnedPars = sum(~self.parIsPinned) # prefixed tilde does a boolean inversion in python; built-in 'sum()' will count true instances of boolean lists.
    self.indicesUnpinnedPars = nu.zeros([self.numUnpinnedPars],nu.integer)
    j = 0
    for i in range(self.numPars):
      if self.parIsPinned[i]: continue
      self.indicesUnpinnedPars[j] = i
      j = j + 1

###    self._deskewTransMatrix   = None
###    self._deskewUntransMatrix = None

    if transformIDs==None:
      self._transformIDs = nu.zeros([self.numPars], nu.int)
    else:
      self._transformIDs = transformIDs

    self._extraTransformsList = extraTransformsList
    self._transformsList = [trn.TransformIdentity()]+extraTransformsList
    self._derivsMatrix = None
    self._derivsMatrixInv = None

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def transform(self, untransParValues, untransCovarMat=None):
    """
The parameters used to define the model can be transformed for greater convenience during the fitting routine. This transform is broken into two parts here. Mathematically the transform is specified by

	q'_ = F_(q_).

The vectors q_ and q'_ represent respectively the original and transformed parameters. F_ is a vector of functions. (At present the kth component of F_ must take only the kth component of q_ as its argument - multi-parameter functions are not yet implemented.) A example might be [q_0, ln(q_1), q_2, q_3, q_4^2].

The equivalent (linearized, thus approximate) transform of the covariance matrix has the following form:

	C' = D * C * D^T
where
	           d(F_k)
	D_{k,l} = --------.
	           d(q_l)

With the current single-argument restrictions on F_() it is easy to see that D will be diagonal.
    """
    parValues = untransParValues.copy()
    for i in range(self.numPars):
      parValues[i] = self._transformsList[self._transformIDs[i]].transform(untransParValues[i])

    if untransCovarMat!=None:
      if nu.any(self._transformIDs>0): # saves time when there are only identity transforms.
        self._constructDerivsMatrix(untransParValues)
        covarMatrix = ma.transformCovarMat(self._derivsMatrix, untransCovarMat)
      else:
        covarMatrix = untransCovarMat.copy()

###    if self._deskewTransMatrix!=None:
###      parValues = mu.matMul(self._deskewTransMatrix, parValues)

    if untransCovarMat==None:
      return parValues
###    else:
###      if self._deskewTransMatrix!=None:
###        covarMatrix = ma.transformCovarMat(self._deskewTransMatrix, covarMatrix)

    return (parValues, covarMatrix)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def deTransform(self, transParValues, transCovarMat=None):
    """
See docstring for transform(). Everything is (necessarily) reverse in order here.
    """
###    if self._deskewUntransMatrix==None:
###      parValues = transParValues.copy()
###    else:
###      parValues = mu.matMul(self._deskewUntransMatrix, transParValues)
    parValues = transParValues.copy()

    if transCovarMat!=None:
###      if self._deskewUntransMatrix==None:
###        covarMatrix = transCovarMat.copy()
###      else:
###        covarMatrix = ma.transformCovarMat(self._deskewUntransMatrix, transCovarMat)
      covarMatrix = transCovarMat.copy()

    for i in range(self.numPars):
      parValues[i] = self._transformsList[self._transformIDs[i]].deTransform(parValues[i])

    if transCovarMat==None:
      return parValues
    else:
      if nu.any(self._transformIDs>0): # saves time when there are only identity transforms.
        self._constructDerivsMatrix(parValues)
        covarMatrix = ma.transformCovarMat(self._derivsMatrixInv, covarMatrix)

    return (parValues, covarMatrix)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def transformDerivs(self, derivs, parValues):
    """
See docstring for transform() for nomenclature.

Suppose we want to calculate derivatives, wrt one of the parameters q_k, of some function m(q'_) of the transformed parameters. (In actuality the present method works it the other way.) By the chain rule,

	  d(m)        d(m)     d(q'_1)          d(m)     d(q'_M)
	--------- = ---------*--------- + ... ---------*---------.
	 d(q_k)      d(q'_1)   d(q_k)          d(q'_M)   d(q_k)

Now as detailed in the docstring for method transform(),

	q'_j(q_) = F_(q_),

thus

	 d(q'_j)
	--------- = D_{.,k};
	 d(q_k)

and in fact the whole transform can be expressed as

	d_ = D * d'_,
where
	         d(m)
	d'_k = ---------
	        d(q'_k)

etc. As mentioned, here we want to do the reverse:

	d'_ = D^{-1} * d_.
    """    

    transDerivs = derivs.copy()

    if nu.any(self._transformIDs>0): # saves time when there are only identity transforms.
      self._constructDerivsMatrix(parValues)

###      if self._deskewUntransMatrix==None:
###        deTransMatrix = self._derivsMatrixInv.copy()
###      else:
###        deTransMatrix = mu.matMul(self._derivsMatrixInv, self._deskewUntransMatrix)
      deTransMatrix = self._derivsMatrixInv.copy()

    else:
###      if self._deskewUntransMatrix==None:
###        return transDerivs
###      else:
###        deTransMatrix = self._deskewUntransMatrix.copy()
      return transDerivs

    for ri in range(self.numPars):
      summ = nu.zeros(derivs.shape[:-1], nu.float)
      for ci in range(self.numPars):
        summ += deTransMatrix[ri,ci] * derivs[...,ci]
      transDerivs[...,ri] = summ

    return transDerivs

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def transformDerivWrtParK(self, derivWrtParK, parValues, k, doRecalcDerivsMatrix=True):
    """
See docstring for transformDerivs().
    """
#### Note that this routine can NOT be implemented if the transform involves mixing between parameters. I.e. it assumes that self._derivsMatrixInv is diagonal.

    if doRecalcDerivsMatrix and nu.any(self._transformIDs>0):
      self._constructDerivsMatrix(parValues)

    if self._transformIDs[k]==0: # saves time when there are only identity transforms.
      transDerivWrtParK = derivWrtParK.copy()
    else:
      transDerivWrtParK = self._derivsMatrixInv[k,k] * derivWrtParK
      if self._tf:
        print 'In ParSpecifications.transformDerivWrtParK(). k, self._derivsMatrixInv[k,k], derivWrtParK[0], transDerivWrtParK[0]:'
        print k, self._derivsMatrixInv[k,k], derivWrtParK[0], transDerivWrtParK[0]

    return transDerivWrtParK

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def transformSecondDerivs(self, derivs, parValues):
    """
See docstring for transform() for nomenclature.

The reasoning here is similar to that in method transformDerivs(). The end result is that the matrix S' of second derivatives of the model wrt to the transformed parameters is related to S, ditto for the untransformed parameters, by

	S = D * S' * D^T.

In other words, it is the inverse to the relationship between covariance matrices.

As with transformDerivs(), the deTransform is done within loops so as to cater for S matrices which have many dimensions for each element.
    """    

    transDerivs = secondDerivs.copy()

    if nu.any(self._transformIDs>0): # saves time when there are only identity transforms.
      self._constructDerivsMatrix(parValues)

###      if self._deskewUntransMatrix==None:
###        kMatrix = self._derivsMatrixInv.copy()
###      else:
###        kMatrix = mu.matMul(self._derivsMatrixInv, self._deskewUntransMatrix)
      kMatrix = self._derivsMatrixInv.copy()

    else:
###      if self._deskewUntransMatrix==None:
###        return transDerivs
###      else:
###        kMatrix = self._deskewUntransMatrix.copy()
      return transDerivs

    for ri in range(self.numPars):
      for ci in range(self.numPars):
        summ = nu.zeros(derivs.shape[:-2], nu.float)
        for ai in range(self.numPars):
          for bi in range(self.numPars):
            summ += deTransMatrix[ri,bi] * secondDerivs[...,bi,ai] * deTransMatrix[ci,ai]
        transDerivs[...,ri,ci] = summ

    return transDerivs

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def transformSecondDerivWrtParsKL(self, derivWrtParsKL, parValues, k, l\
    , doRecalcDerivsMatrix=True):
    """
See docstring for transformSecondDerivs().
    """    
#### Note that this routine can NOT be implemented if the transform involves mixing between parameters. I.e. it assumes that self._derivsMatrixInv is diagonal.

    if doRecalcDerivsMatrix and nu.any(self._transformIDs>0):
      self._constructDerivsMatrix(parValues)

    transDerivWrtParsKL = derivWrtParsKL.copy()
    if self._transformIDs[k]>0:
      transDerivWrtParsKL *= self._derivsMatrixInv[k,k]
    if self._transformIDs[l]>0:
      transDerivWrtParsKL *= self._derivsMatrixInv[l,l]

    return transDerivWrtParsKL

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _constructDerivsMatrix(self, parValues):
    """
As with every other relevant part of the present class, this assumes that parameter transformations don't mix more than 1 parameter. The matrix of derivatives is therefore diagonal.
    """
    self._derivsMatrix    = nu.diag(nu.ones([self.numPars], nu.float))
    self._derivsMatrixInv = nu.diag(nu.ones([self.numPars], nu.float))
    for k in range(self.numPars):
      if self._transformIDs[k]>0:
        element = self._transformsList[self._transformIDs[k]].calcDeriv(parValues[k])
        self._derivsMatrix[   k,k] = element
        self._derivsMatrixInv[k,k] = 1.0/element

      if self._tf:
        print 'In ParSpecifications._constructDerivsMatrix(). k, element:', k, element


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def copy(self):
    return ParSpecifications(self.parNames[:], self.parUnits[:], self.parIsPinned.copy()\
      , self.priors.copy(), self._transformIDs.copy(), self._extraTransformsList[:])

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _strCore(self, spaces=''):
    myStr  = spaces+'  Columns: number, is pinned, transform ID, name, unit.\n'
    for i in range(self.numPars):
      myStr += spaces+'    %3d %5s %3d %s %s\n' % (i, self.parIsPinned[i]\
        , self._transformIDs[i], self.parNames[i], self.parUnits[i])

    myStr += spaces+'  Transforms:\n'
    for i in range(len(self._transformsList)):
      myStr += spaces+'    %3d %s\n' % (i, self._transformsList[i].__class__.__name__)

    myStr += spaces+'  Priors:\n'
    myStr += self.priors.__str__(spaces+'    ')
    return myStr

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def __str__(self, spaces=''):
    me = 'parameter.ParSpecifications'
    myStr  = spaces+'<%s instance.\n' % (me)
    myStr += self._strCore(spaces)
    myStr += spaces+'>\n'
    return myStr

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def __repr__(self):
    myStr = 'ParSpecifications(%r, %r, %r, %r, %r, %r)' % (self.parNames\
      , self.parUnits, self.parIsPinned, self.priors, self._transformIDs\
      , self._extraTransformsList)
    return myStr


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__=='__main__':
  pass




























