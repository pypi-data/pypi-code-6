#!/usr/bin/env python

# Name:                         paramz_models
#
# Author: Ian Stewart
#
# TODO:
#	- Test harness has not so far been touched - may need work.
#
# Contents:
#	class RValuesGrid:
#	class _ValueOnGrid:
#	class _ParameterizedModel(_ModelOnGrid):
#	class _LinearModel(_ParameterizedModel):
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
# - Deleted test harness.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
This module is intended to contain a superclass to define the basic framework for a function which depends on a number of parameters. The class also stores details of the shape of the assembly of independant variables.
"""

_module_name = 'paramz_models'

import numpy as nu

#import ims_exceptions as ex
import local_exceptions as ex
import math_utils as ma

_tf=False

#.......................................................................
class RValuesGrid:
  """
This defines a rectilinear grid of values of the independent variable r_.
  """
  def __init__(self, listOfAxesVectors):
    self._listOfAxesVectors = listOfAxesVectors # expected to be a simple list, each element of which is a 1D numpy array of floats recording the value of that coordinate of the grid.
    self.shape = ()
    for axesVector in self._listOfAxesVectors:
      self.shape += (len(axesVector),)

  def __getitem__(self, k):
    return self._listOfAxesVectors[k]

#.......................................................................
class _ValueOnGrid:
  """
This is the parent class of every object in the present module, because in every case there is an assumption that values are going to be calculated which fall on a rectilinear grid. These values may themselves be array objects of any dimensionality (including simple scalars).
  """
  def __init__(self, rValuesObject, dataType=type(1.0), elementShape=(1,)):
    """
Explanation of arguments:

	- rValuesObject: an object of type RValuesGrid. This specifies the grid of the independent variable r_. It is expected to behave like a list, the jth element of which is a numpy vector of floats giving the coordinates of the r_ grid points in the direction of the jth axis. It should also have an attribute 'shape' which records the dimensions of all the axes.

	- dataType: fairly self-explanatory. Default is 'float'.

	- elementShape: array shape for the objects which are defined at each r_. Default is scalar.
    """
    self.rValuesObject = rValuesObject
    self.dataType      = dataType
    self.elementShape  = elementShape

    self.numRValues = nu.prod(self.rValuesObject.shape)

    if len(self.elementShape)==1 and self.elementShape[0]==1:
      self.elementsAreScalar = True
      self.totalShape      = self.rValuesObject.shape
      self.totalShapeCovar = self.rValuesObject.shape
    else:
      self.elementsAreScalar = False
      self.totalShape      = self.rValuesObject.shape+self.elementShape
      self.totalShapeCovar = self.rValuesObject.shape+self.elementShape+self.elementShape # for e.g. storing covariances between items in the array for each data element, or 2nd derivatives of functions of the model elements.

#.......................................................................
class _ParameterizedModel(_ValueOnGrid):
  """
This is designed to serve as a superclass for any kind of function class which stores a sequence or array of values of the independent variable 'r', and which can be asked to calculate matching model function values. These values are calculated from a formula, specific to the particular subclass, but which depends on a number of parameters.

One feature of the present class is that its function is an N-value function of N independent variables (not counting the parameters) (also, the values are not necessarily scalars).

Built into the present class is the assumption that the parameters will usually need to be processed outside the model itself in some sort of transformed form. This might be to make the expected distribution of values of a parameter more even and thus to facilitate fitting. Whereever the parameters are used in the model, they should be detransformed first, using the deTransform() method of the parsSpecObj.

Methods which are implemented in the present superclass:
	__init__()
	calcModelValue()
	_calcModelValueTrans()
	calcModelValues()
	_calcModelValuesTrans()
	setModelValues()
	_setModelValuesTrans()
	_setModelValuesUntrans()
	calcDMByDParK()
	_calcDMByDParKTrans()
	calcD2MByDParKParL()
	_calcD2MByDParsKLTrans()
	_estFirstDerivByFDTrans()
	_estSecondDerivByFDTrans()
	_calcAllFirstDerivsTrans()
	_calcAllSecondDerivsTrans()

Methods which instead need to be implemented by subclasses are:
	_calcModelValueUntrans()
	_calcModelValuesUntrans()
	_calcDMByDParKUntrans()
	_calcD2MByDParsKLUntrans()
  """
  _tf=False

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def __init__(self, parsSpecObj, rValuesObject, dataType=type(1.0), elementShape=(1,)):
    """
Explanation of the arguments:

	- parsSpecObj: an object of type ParSpecifications. This contains methods such as deTransform() which can be used to return the parameters to the form the model can deal with. It also contains the parameter names and units, and whether any are 'pinned', i.e. not desired to be fitted.

	- rValuesObject: this contains information about the samples of the independent variable. It should have the attribute 'shape' and be suitable for processing within methods _calcModelValuesWithUntrans(), _calcDMByDParKWithUntrans() and _calcD2MByDParsKLWithUntrans(). The model is expected to define 1 element (not necessarily a scalar) for each sample. The class RValuesGrid offers a template for this type of object.

	- dataType: self-explanatory

	- elementShape: tuple giving the arrangement of elements in each model sample.
    """
    self.parsSpecObj = parsSpecObj
    _ValueOnGrid.__init__(self, rValuesObject, dataType, elementShape)

    self.mValues = None
    self.numPars = self.parsSpecObj.numPars # to support old code which still looks for this in the present class! Also for the sake of brevity.

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def calcModelValue(self, parValues, rValue, parsAreTrans=False):
    if parsAreTrans:
      return self._calcModelValueTrans(parValues, rValue)
    else:
      return self._calcModelValueUntrans(parValues, rValue)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcModelValueTrans(self, transParValues, rValue):
    parValues = self.parsSpecObj.deTransform(transParValues)
    modelValue = self._calcModelValueUntrans(parValues, rValue)
    return modelValue

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcModelValueUntrans(self, parValues, rValue):
    raise ex.EmptyMethod()


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def calcModelValues(self, parValues, parsAreTrans=False):
    if parsAreTrans:
      return self._calcModelValuesTrans(parValues)
    else:
      return self._calcModelValuesUntrans(parValues)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcModelValuesTrans(self, transParValues):
    parValues = self.parsSpecObj.deTransform(transParValues)
    modelValues = self._calcModelValuesUntrans(parValues)
    return modelValues

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcModelValuesUntrans(self, parValues):
    raise ex.EmptyMethod()


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def setModelValues(self, parValues, parsAreTrans=False):
    if parsAreTrans:
      self._setModelValuesTrans(parValues)
    else:
      self._setModelValuesUntrans(parValues)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _setModelValuesTrans(self, transParValues):
    mValues = self._calcModelValuesTrans(transParValues)
    if mValues==None:
      self.mValues = None
    else:
      self.mValues = mValues.copy()

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _setModelValuesUntrans(self, parValues):
    mValues = self._calcModelValuesUntrans(parValues)
    if mValues==None:
      self.mValues = None
    else:
      self.mValues = mValues.copy()


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def calcDMByDParK(self, parValues, k, doRecalcMValues=True, parsAreTrans=False):
    if parsAreTrans:
      return self._calcDMByDParKTrans(parValues, k, doRecalcMValues)
    else:
      return self._calcDMByDParKUntrans(parValues, k, doRecalcMValues)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcDMByDParKTrans(self, transParValues, k, doRecalcMValues=True):
    parValues = self.parsSpecObj.deTransform(transParValues)
    derivArray = self._calcDMByDParKUntrans(parValues, k, doRecalcMValues)
    transDerivArray = self.parsSpecObj.transformDerivWrtParK(derivArray, parValues, k, doRecalcMValues)
    return transDerivArray

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcDMByDParKUntrans(self, parValues, k, doRecalcMValues=True):
    raise ex.EmptyMethod()
    if doRecalcMValues:
      self.setModelValues(parValues)
    #return derivArray # here as a placeholder to show the expected interface. Should return the calculated array of model-function derivatives wrt parameter number k.


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def calcD2MByDParKParL(self, parValues, k, l, doRecalcMValues=True, parsAreTrans=False):
    if parsAreTrans:
      return self._calcD2MByDParsKLTrans(  parValues, k, l, doRecalcMValues)
    else:
      return self._calcD2MByDParsKLUntrans(parValues, k, l, doRecalcMValues)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcD2MByDParsKLTrans(self, transParValues, k, l, doRecalcMValues=True):
    parValues = self.parsSpecObj.deTransform(transParValues)
    derivArray = self._calcD2MByDParsKLUntrans(parValues, k, l, doRecalcMValues)
    transDerivArray = self.parsSpecObj.transformSecondDerivWrtParsKL(derivArray, parValues, k, l, doRecalcMValues)
    return transDerivArray

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcD2MByDParsKLUntrans(self, parValues, k, l, doRecalcMValues=True):
    raise ex.EmptyMethod()
    if doRecalcMValues:
      self.setModelValues(parValues)
    #return derivArray # here as a placeholder to show the expected interface. Should return the calculated array of model-function second derivatives wrt parameter numbers k and l.


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def estFirstDerivByFD(self, parValues, k, dPar, parsAreTrans=False):
    if parsAreTrans:
      return self._estFirstDerivByFDTrans(  parValues, k, dPar)
    else:
      return self._estFirstDerivByFDUntrans(parValues, k, dPar)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _estFirstDerivByFDTrans(self, transParValues, k, dPar):
    raise ex.EmptyMethod()

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _estFirstDerivByFDUntrans(self, parValues, k, dPar):
    """
Performs a finite-difference estimate of the first derivative of the model function wrt parameter k.

Returns an array which has shape==self.totalShape.
    """
    diffValuesNumeric = ma.finiteDifference(self._calcModelValuesUntrans, parValues, [{'index':k,'delta':dPar}])
    return diffValuesNumeric


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def estSecondDerivByFD(self, parValues, k, l, dParK, dParL, parsAreTrans=False):
    if parsAreTrans:
      return self._estSecondDerivByFDTrans(  parValues, k, l, dParK, dParL)
    else:
      return self._estSecondDerivByFDUntrans(parValues, k, l, dParK, dParL)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _estSecondDerivByFDTrans(self, transParValues, k, l, dParK, dParL):
    raise ex.EmptyMethod()

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _estSecondDerivByFDUntrans(self, parValues, k, l, dParK, dParL):
    """
Performs a finite-difference estimate of the second derivative of the model function wrt parameters k and l.

Returns an array which has shape==self.totalShape.
    """
    deltaList = [{'index':k,'delta':dParK},{'index':l,'delta':dParL}]
    diffValuesNumeric = ma.finiteDifference(self._calcModelValuesUntrans, parValues, deltaList)
    return diffValuesNumeric


  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcAllFirstDerivsTrans(self, transParValues, doRecalcMValues=True):
###### introduce generic method, following the same pattern as the others above.
    """
In the present method we want to set up an array to contain the derivatives of the model function w.r.t each of the parameters. The rank of this array must therefore be 1 more than the rank of self.mValues.
    """    

    parValues = self.parsSpecObj.deTransform(transParValues)

    derivShape = self.totalShape+(self.numPars,)
    derivs = nu.zeros(derivShape, self.dataType)
    noLoopPasses = True
    for k in range(self.numPars):
      derivs[...,k] = self._calcDMByDParKUntrans(parValues, k, (noLoopPasses and doRecalcMValues))
      noLoopPasses = False

    return self.parsSpecObj.transformDerivs(derivs, parValues)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcAllSecondDerivsTrans(self, transParValues, doRecalcMValues=True):
    """
Here we want to set up an array to contain the second derivatives of the model function w.r.t each of the parameters. The rank of this array must therefore be 2 more than the rank of self.mValues.
    """

    parValues = self.parsSpecObj.deTransform(transParValues)

    derivShape = self.totalShape+(self.numPars,self.numPars,)
    secondDerivs = nu.zeros(derivShape, self.dataType)
    noLoopPasses = True
    for k in range(self.numPars):
      secondDerivs[...,k,k] = self._calcD2MByDParsKLUntrans(parValues, k, k, (noLoopPasses and doRecalcYValues))
      noLoopPasses = False
      for l in range(k+1, self.numPars):
        secondDerivs[...,k,l] = self._calcD2MByDParsKLUntrans(parValues, k, l, False)
        secondDerivs[...,l,k] = secondDerivs[...,k,l]

    return self.parsSpecObj.transformSecondDerivs(secondDerivs, parValues)

###  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
###  def setHessianParTransform(self, transMatrix, untransMatrix):
###    self.parsSpecObj._deskewTransMatrix   = transMatrix
###    self.parsSpecObj._deskewUnTransMatrix = untransMatrix


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__=='__main__':
  pass
