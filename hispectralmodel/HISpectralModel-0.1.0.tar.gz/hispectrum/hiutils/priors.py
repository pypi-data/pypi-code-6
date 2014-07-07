#!/usr/bin/env python

# Name:                         priors
#
# Author: Ian Stewart
#
# Contents:
#	class _LnPriors:
#	class LnPriorsFlat(_LnPriors):
#	class LnPriorsSeparable(_LnPriors):
#	class _LnPrior:
#	class _LnPriorSeparable(_LnPrior):
#	class _LnPriorGauss(_LnPriorSeparable):
#	class PriorGauss(_LnPriorGauss):
#	class PriorTruncGauss(_LnPriorGauss):
#	class PriorTruncGaussLo(_LnPriorGauss):
#	class PriorTruncGaussHi(_LnPriorGauss):
#	class PriorGamma(_LnPriorSeparable):
#	class _LnPriorExp(_LnPriorSeparable):
#	class PriorExp(_LnPriorExp):
#	class PriorTruncExp(_LnPriorExp):
#	class PriorRayleigh(_LnPriorSeparable):
#	class PriorLogRayleigh(_LnPriorSeparable):
#	class PriorTopHat(_LnPriorSeparable):
#	class PriorPiecewisePower(_LnPriorSeparable):
#	class PriorPiecewiseExp(_LnPriorSeparable):
#	class PriorDeltaFunction(_LnPriorSeparable):
#	class PriorLorentzian(_LnPriorSeparable):
#	class PriorJeffreys(_LnPriorSeparable):
#	class _LnPriorImproper(_LnPriorSeparable):
#	class PriorImproper(_LnPriorImproper):
#	class PriorImproperLo(_LnPriorImproper):
#	class PriorImproperHi(_LnPriorImproper):
#	class PriorSine(_LnPriorSeparable):
#	def getPrior(priorTypeStr, info):
#
# TODO:
#	- Check that the bootstrapping theory (in particular the division by root 2) is correct!
#	- Implement reading, writing and __str__ of optional range in improper prior.
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
# * Copied to this release version. Deleted test harness and made some other slight changes.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""Class definitions and utility functions to deal with prior probability functions."""

_module_name = 'priors'

import math
import numpy as nu
from scipy import special as sp

#import ims_exceptions as ex
import local_exceptions as ex
import misc_utils as mu
#import SciMathConstants as const
import math_utils as ma
import ranges as ra
#import read_valid_lines as rvl
import random_aux as rna

_testFlag = False

_forPriorVersionStr = '6' # continues on from the numbering in bayes_parameter.py.
_firstLine = '_version\t%s' % (_forPriorVersionStr)
_numNonPriorLines = 1
_numGenericColumns = 1

_maxNumPriorInfoCols = 4

_rootTwo = math.sqrt(2.0)
_rootPi  = math.sqrt(math.pi)

#.......................................................................
class _LnPriors:
  """
Superclass for the joint prior distribution of all model parameters.
  """
  separable = False # default

  def calcValue(self, parValues):
    raise ex.EmptyMethod()
    # return scalar float

  def calcGradient(self, parValues):
    raise ex.EmptyMethod()
    # return 1D numpy array of floats

  def calcHessian(self, parValues):
    raise ex.EmptyMethod()
    # return 2D numpy array of floats

  def priorsDistributedRandoms(self, size):
    raise ex.EmptyMethod()
    # return 1D numpy array of floats

  def unflatten(self, pointInFlatPrior):
    raise ex.EmptyMethod()

  def calcDistanceToBound(self, parValues, parDeltas):
    """
Calculates the distance, in multiples of |parDeltas|, starting from parValues and in the direction of parDeltas, to that point where the prior probability density decreases to zero.

The method should raise an exception if self.calcLnPriors(parValues)==None.

If there is no bound in the direction specified, the method should return 'None'.
    """
    raise ex.EmptyMethod()
    # return scalar float ('None' if there is no bound in that direction)

  def _getInfo(self):
    raise ex.EmptyMethod()

  def copy(self):
    raise ex.EmptyMethod()

#.......................................................................
class LnPriorsFlat(_LnPriors):
  """
This is a convenient class for the case when we don't want to be bothered with priors, we take them all improper for every parameter.
  """
  separable = True

  def __getitem__(self, i):
    return PriorFlatImproper()

  def calcValue(self, parValues):
    return 0.0

  def calcGradient(self, parValues):
    return nu.zeros([len(parValues)], nu.float)

  def calcHessian(self, parValues):
    numPars = len(parValues)
    return nu.zeros([numPars,numPars], nu.float)

  def unflatten(self, pointInFlatPrior):
    raise 'cannot unflatten an improper prior'

  def calcDistanceToBound(self, parValues, parDeltas):
    return (None, None, None)

  def _getInfo(self):
    raise ex.EmptyMethod()

  def copy(self):
    return LnPriorsFlat()

  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.>\n' % (_module_name, self.__class__.__name__)
    return myStr

  def __repr__(self):
    myStr = 'LnPriorsFlat()'
    return myStr

#.......................................................................
class LnPriorsSeparable(_LnPriors):
  """
A class to define priors where the joint prior can be decomposed into a product of the priors for individual parameters.
  """
  separable = True

  def __init__(self, listOfSeparablePriors):
    self._listOfSeparablePriors = listOfSeparablePriors

  def len(self):
    return len(self._listOfSeparablePriors)

  def __getitem__(self, i):
    return self._listOfSeparablePriors[i]

  def __setitem__(self, i, prior):
    self._listOfSeparablePriors[i] = prior

  def calcValue(self, parValues):
#    print 'At priors.py line 220'
#    print '>>> parValues.shape', parValues.shape
    totalLnPriorValue = 0.0
    for i in range(len(self._listOfSeparablePriors)):
      prior = self._listOfSeparablePriors[i]
      lnPriorValue = prior.calcLnPrior(parValues[i])
#      if i==3: print 'in PriorsSeparable.calcLnPrior(). i, lnPriorValue:', i, lnPriorValue
      if lnPriorValue==None:
        return None

      totalLnPriorValue += lnPriorValue

    return totalLnPriorValue

  def calcGradient(self, parValues):
    numPars = len(parValues)
    derivsOfLn = nu.zeros([numPars], nu.float)
    for i in range(numPars):
      prior = self._listOfSeparablePriors[i]
      derivsOfLn[i] = prior.calcDerivOfLn(parValues[i])

    return derivsOfLn

  def calcHessian(self, parValues):
    numPars = len(parValues)
    derivsOfLn = nu.zeros([numPars,numPars], nu.float)
    for i in range(numPars):
      prior = self._listOfSeparablePriors[i]
      derivsOfLn[i,i] = prior.calc2ndDerivOfLn(parValues[i])

    return derivsOfLn

  def unflatten(self, pointInFlatPrior):
    numPars = len(pointInFlatPrior)
    parValues = nu.zeros([numPars], nu.float)
    for i in range(numPars):
      prior = self._listOfSeparablePriors[i]
      parValue = prior.unflatten(pointInFlatPrior[i])

      if parValue==None:
        return None

      parValues[i] = parValue

    return parValues

  def calcDistanceToBound(self, parValues, parDeltas):
    """
This method calculates the distance, in multiples of |parDeltas|, starting from parValues and in the direction of parDeltas, to that point where the prior probability density decreases to zero.

An exception is raised if self.calcLnPriors(parValues)==None.

If there is no bound in the direction specified, 'None' is returned.
    """
    if self.calcValue(parValues)==None:
      raise 'improper start'

    numPars = len(parValues)
    distancesToBound = []
    boundIsLower = []
    for i in range(numPars):
      prior = self._listOfSeparablePriors[i]
      try:
        myRange = prior.priorRange
      except AttributeError:
        distancesToBound.append(None)
        boundIsLower.append(None)
        continue

      if   parDeltas[i]>0.0:
        if myRange.hi==None:
          distancesToBound.append(None)
          boundIsLower.append(None)
        else:
          distancesToBound.append(-(myRange.hi-parValues[i])/parDeltas[i]) # the negation is because we want the smallest +ve distance. We are not storing any negative ones, so one might think we could just store the +ve ones unaltered and then do min(distancesToBound) at the end. However it seems that None values are judged to be smaller than any +ve value. Hence the negation, and a -max() at the end instead of a min.
          boundIsLower.append(False)
      elif parDeltas[i]<0.0:
        if myRange.lo==None:
          distancesToBound.append(None)
          boundIsLower.append(None)
        else:
          distancesToBound.append(-(myRange.lo-parValues[i])/parDeltas[i])
          boundIsLower.append(True)
      else: # parDeltas[i]==0.0
        distancesToBound.append(None)
        boundIsLower.append(None)

    if max(distancesToBound)==None: # means all the entries are None.
      return (None, None, None)
    else:
      indexOfMax = mu.maxloc(distancesToBound)
      return (indexOfMax, -distancesToBound[indexOfMax], boundIsLower[indexOfMax])

  def _getInfo(self):
    numPars = len(self._listOfSeparablePriors)
    typesList = []
    priorElementIs = nu.ones([numPars],nu.int)
#    priorInfos = nu.zeros([_maxNumPriorInfoCols, numPars], nu.float)
    priorInfos = nu.ma.zeros([_maxNumPriorInfoCols, numPars], nu.float) # now a masked array.
    priorInfos.mask = nu.ma.zeros([_maxNumPriorInfoCols, numPars], nu.bool)
    for i in range(numPars):
      prior = self._listOfSeparablePriors[i]
      typesList.append(prior.priorType)
      priorInfo = prior.getInfo()
      priorInfos[:len(priorInfo),i] = priorInfo
      priorInfos[len(priorInfo):,i].mask = True

    return (nu.array(typesList), priorElementIs, priorInfos)

#  def __str__(self):
#    myStr  = '<%s object.\n' % (self.__class__.__name__)
#    numPars = len(self._listOfSeparablePriors)
#    for i in range(numPars):
##      myStr += '  Prior %d:\n' % (i)
#      myStr += '  Prior %d: ' % (i)
#      myStr += self._listOfSeparablePriors[i].__str__(spaces='  ')+'\n'
#    return myStr+'>'

  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    numPars = len(self._listOfSeparablePriors)
    for i in range(numPars):
      myStr += spaces+'  Prior %d:\n' % (i)
      myStr += self._listOfSeparablePriors[i].__str__(spaces+'    ')
    myStr += spaces+'>\n'
    return myStr

  def __repr__(self):
    myStr = 'LnPriorsSeparable(%r)' % (self._listOfSeparablePriors)
    return myStr

  def copy(self):
    return LnPriorsSeparable(self._listOfSeparablePriors[:])

#.......................................................................
class _LnPrior:
  """This is intended to be a superclass for an object which encodes the prior probability distribution of a single model parameter as used in Bayesian model estimation."""
#  def __init__(self, parameterName, unitStr, isLog10, delta, isJoint):

  def calcLnPrior(self, value):
    raise ex.EmptyMethod()

  def calcDerivOfLn(self, value):
    raise ex.EmptyMethod()

  def calc2ndDerivOfLn(self, value):
    raise ex.EmptyMethod()

  def priorDistributedRandoms(self, size):
    raise ex.EmptyMethod()

  def unflatten(self, flatParValue):
    """
Let's define a variable y such that

	     x
	    /
	y = | dx' p(x')
	    /
	  -inf

where p(x) is the normalized prior. Then y will be found within the interval [0,1]. The method unflatten() defines the reverse transform, i.e.

	x = self.unflatten(y).

    """
    if flatParValue<0.0 or flatParValue>=1.0:
      return None
    return self._unflatten(flatParValue)

  def _unflatten(self, flatParValue):
    raise ex.EmptyMethod()

#  def __str__(self):
#    myStr  = '<%s object.\n' % (self.__class__.__name__)
#    myStr += '  Parameter name  = %s\n' % (self.name)
#    myStr += '  Units           = %s\n' % (self.unitStr)
#    myStr += '  Delta value     = %e\n' % (self.delta)
#    myStr += '  Is it a log10 type? %s\n' % (self.isLog10)
##    myStr += 'Is it joint? %s\n' % (self.isJoint)
#    return myStr

  def getInfo(self):
    return nu.zeros([0],nu.float)

  def copy(self):
    raise ex.EmptyMethod()

##.......................................................................
#class _LnPriorJoint(_LnPrior):
#  """This is intended to be a superclass for an object which contains functionality etc desired from a model parameter for use in Bayesian model estimation. 'Joint' means that the prior PDF is a non-separable function of more than 1 parameter."""
#  def __init__(self, name, unitStr, isLog10, delta, indexOfMaster):
#    _LnPrior.__init__(self, name, unitStr, isLog10, delta, True)
#    self.priorType = 'joint'
#    self.indexOfMaster = indexOfMaster
#
#  # The _LnPriorJoint object associated with the 'master' parameter should implement the methods calcLnPrior and priorDistributedRandoms. This is expected to be done in an external routine. The methods of the same name attached to the other _LnPriorJoint objects (all those which are not the master in other words) remain unimplemented, since they are never called.
#
#  def __str__(self):
#    myStr  = _LnPrior.__str__(self)
#    myStr += '  Type of prior   = %s\n' % (self.priorType)
#    myStr += '  Index of master = %d\n' % (self.indexOfMaster)
#    return myStr
#
#  def copy(self):
#    raise ex.EmptyMethod()

#.......................................................................
class _LnPriorSeparable(_LnPrior):
  """This is intended to be a superclass for an object which contains functionality etc desired from a model parameter for use in Bayesian model estimation. The 'separable' means that the posterior probability can be expressed in terms of the prior probability distribution for the relevant parameter, times the priors for all the other parameters (whether separable or not), times the likelihood."""
  def __init__(self, priorType):
#    _LnPrior.__init__(self, name, unitStr, isLog10, delta, False)
    self.priorType = priorType

#  def __str__(self):
#    myStr  = _LnPrior.__str__(self)
#    myStr += '  Type of prior   = %s\n' % (self.priorType)
#    return myStr

  def copy(self):
    raise ex.EmptyMethod()

#.......................................................................
class _LnPriorGauss(_LnPriorSeparable):
  def __init__(self, typeStr, priorCentre, priorSigma, priorRange):
    _LnPriorSeparable.__init__(self, typeStr)
    self.priorCentre = priorCentre
    self.priorSigma  = priorSigma
    self.priorRange  = priorRange

    self._recalculate()

  def _recalculate(self):
    norm = ma.integralOfGaussian(self.priorSigma, self.priorCentre, self.priorRange.lo, self.priorRange.hi)
    self.priorAmp = 1.0 / norm
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    if not self.priorRange.contains(x):
      return None
    arg = (x - self.priorCentre) / self.priorSigma
    return self.priorLnAmp - arg*arg/2.0

  def calcDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return (self.priorCentre - x) / self.priorSigma / self.priorSigma

  def calc2ndDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return -1.0 / self.priorSigma / self.priorSigma

  def priorDistributedRandoms(self, size=1):
    randoms = nu.array(rna.getTruncGaussRandoms(self.priorSigma\
      , size, self.priorCentre, self.priorRange.lo, self.priorRange.hi\
      , 'simple')) # chose style=='simple' because presumably the truncations will usually be minor - the Gaussian character of the distribution disappears if the truncation is too radical - in this case we would expect some other prior to be used.
#    print randoms
#    print randoms.shape

#    if size<=1:
#      return randoms[0]
#    else:
#      return randoms
    return randoms

  def _unflatten(self, flatParValue):
#    tempValue = flatParValue * const.rootTwo / const.rootPi / self.priorSigma / self.priorAmp
    tempValue = flatParValue * _rootTwo / _rootPi / self.priorSigma / self.priorAmp
    if self.priorRange.lo==None:
      tempValue -= 1.0
    else:
#      tempValue += sp.erf((self.priorRange.lo - self.priorCentre) / self.priorSigma / const.rootTwo)
      tempValue += sp.erf((self.priorRange.lo - self.priorCentre) / self.priorSigma / _rootTwo)

#    parValue = self.priorCentre + self.priorSigma * const.rootTwo * sp.erfinv(tempValue)
    parValue = self.priorCentre + self.priorSigma * _rootTwo * sp.erfinv(tempValue)
    return parValue

#  def __str__(self, spaces=''):
#    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
#    myStr += spaces+'    Type: %s\n' % (self.priorType)
#    myStr += spaces+'  Centre: %f\n' % (self.priorCentre)
#    myStr += spaces+'   Sigma: %f\n' % (self.priorSigma)
#    myStr += spaces+'   Range: '+self.priorRange.__repr__(spaces=spaces+'  ')+'\n'
#    return myStr + spaces+'>'


  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'  Centre: %f\n' % (self.priorCentre)
    myStr += spaces+'   Sigma: %f\n' % (self.priorSigma)
    myStr += spaces+'   Range: %r\n' % (self.priorRange)
    myStr += spaces+'>\n'
    return myStr

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]^2 / [2*s^2]) for lo<x<hi, =0 else.\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

#  def getInfo(self):
#    if self.priorRange.lo==None:
#      return nu.array([self.priorCentre, self.priorSigma])
#    else:
#      return nu.array([self.priorCentre, self.priorSigma, self.priorRange.lo, self.priorRange.hi])
#
#  def copy(self):
#    return PriorTruncGauss(self.priorCentre, self.priorSigma, self.priorRange.copy())

#.......................................................................
class PriorGauss(_LnPriorGauss):
  def __init__(self, priorCentre, priorSigma):
    _LnPriorGauss.__init__(self, 'gauss', priorCentre, priorSigma, ra.SimpleRange())

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]^2 / [2*s^2]) for lo<x<hi, =0 else.\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorCentre, self.priorSigma])

#  def unflatten(self, flatParValue):
#    parValue = self.priorCentre + self.priorSigma * const.rootTwo * sp.erfinv(2.0*flatParValue - 1.0)
#    return parValue

  def copy(self):
    return PriorGauss(self.priorCentre, self.priorSigma)

#.......................................................................
class PriorTruncGauss(_LnPriorGauss):
  def __init__(self, priorCentre, priorSigma, lowerBound, upperBound):
    _LnPriorGauss.__init__(self, 'truncGauss', priorCentre, priorSigma, ra.SimpleRange(lowerBound, upperBound))

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]^2 / [2*s^2]) for lo<x<hi, =0 else.\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorCentre, self.priorSigma, self.priorRange.lo, self.priorRange.hi])

  def copy(self):
    return PriorTruncGauss(self.priorCentre, self.priorSigma, self.priorRange.lo, self.priorRange.hi)

#.......................................................................
class PriorTruncGaussLo(_LnPriorGauss):
  def __init__(self, priorCentre, priorSigma, lowerBound):
    _LnPriorGauss.__init__(self, 'truncGaussLo', priorCentre, priorSigma, ra.SimpleRange(lowerBound, None))

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]^2 / [2*s^2]) for lo<x<hi, =0 else.\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorCentre, self.priorSigma, self.priorRange.lo])

  def copy(self):
    return PriorTruncGaussLo(self.priorCentre, self.priorSigma, self.priorRange.lo)

#.......................................................................
class PriorTruncGaussHi(_LnPriorGauss):
  def __init__(self, priorCentre, priorSigma, upperBound):
    _LnPriorGauss.__init__(self, 'truncGaussHi', priorCentre, priorSigma, ra.SimpleRange(None, upperBound))

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]^2 / [2*s^2]) for lo<x<hi, =0 else.\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorCentre, self.priorSigma, self.priorRange.hi])

  def copy(self):
    return PriorTruncGaussHi(self.priorCentre, self.priorSigma, self.priorRange.hi)

#.......................................................................
class PriorGamma(_LnPriorSeparable):
  def __init__(self, priorAlpha, priorBeta):
    _LnPriorSeparable.__init__(self, 'gamma')
    self.priorAlpha = priorAlpha
    self.priorBeta  = priorBeta
    self.priorRange = ra.SimpleRange(0.0,None)
    self._recalculate()

  def _recalculate(self):
    self.priorLnAmp = self.priorAlpha*math.log(self.priorBeta) - sp.gammaln(self.priorAlpha)
    self.priorAmp = math.exp(self.priorLnAmp)

  def calcLnPrior(self, x):
#	                           b^a r^{a-1}
#	p(r|a,b) = gamma(r|a,b) = ------------- exp(-b*r),
#	                              G(a)
    if not self.priorRange.contains(x):
      return None
    arg = (self.priorAlpha-1.0)*math.log(x) - self.priorBeta.x
    return self.priorLnAmp + arg

  def calcDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return (self.priorAlpha-1.0)/x - self.priorBeta

  def calc2ndDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return -(self.priorAlpha-1.0)/x/x

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()
    return randoms

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = x**(a-1) * exp(-b*x) for x>0, =0 else.\n'
#    myStr += '  a = %e\n' % (self.priorAlpha)
#    myStr += '  b = %e\n' % (self.priorBeta)
#    return myStr + '>'

  def getInfo(self):
    return nu.array([self.priorAlpha, self.priorBeta])

  def copy(self):
    return PriorGamma(self.priorAlpha, self.priorBeta)

#.......................................................................
class _LnPriorExp(_LnPriorSeparable):
  def __init__(self, typeStr, priorScale, priorRange):
    _LnPriorSeparable.__init__(self, typeStr)
    self.priorRange = priorRange
    self.priorScale = priorScale

  def calcLnPrior(self, x):
    if not self.priorRange.contains(x):
      return None
    arg = (x - self.priorRange.lo) / self.priorScale
    return self.priorLnAmp - arg

  def calcDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return -1.0 / self.priorScale

  def calc2ndDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return 0.0

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()
#    randoms = nu.random.standard_exponential(size) / self.priorScale
#    return randoms

  def _unflatten(self, flatParValue):
#    if flatParValue>=1.0 or flatParValue<0.0:
#      return None

    tempValue = 1.0 - flatParValue# / self.priorAmp / self.priorScale
    try:
      parValue = self.priorRange.lo - math.log(tempValue) * self.priorScale
    except ValueError:
      print 'flatParValue, tempValue, self.priorRange.lo, self.priorScale', flatParValue, tempValue, self.priorRange.lo, self.priorScale
      raise
    return parValue

#  def __str__(self, spaces=''):
#    myStr  = spaces+'<%s object.\n' % (self.__class__.__name__)
#    myStr += spaces+'   Scale: %f\n' % (self.priorScale)
#    myStr += spaces+'   Range: '+self.priorRange.__repr__(spaces=spaces+'  ')+'\n'
#    return myStr + spaces+'>'

  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Scale: %f\n' % (self.priorScale)
    myStr += spaces+'   Range: %r\n' % (self.priorRange)
    myStr += spaces+'>\n'
    return myStr

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]/s)\n'
##    myStr += '  x0 = %e\n' % (self.priorStart)
#    myStr += '  s  = %e\n' % (self.priorScale)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

#.......................................................................
class PriorExp(_LnPriorExp):
  def __init__(self, priorScale, lowerBound=0.0): # We expect that this to be called with the lower range bound defined, but not the upper.
    _LnPriorExp.__init__(self, 'exp', priorScale, ra.SimpleRange(lowerBound, None))
    self.priorAmp = 1.0 / self.priorScale
    self.priorLnAmp = math.log(self.priorAmp)

  def priorDistributedRandoms(self, size=1):
    evenRandoms = nu.random.random(size)
    randoms = self.priorRange.lo - self.priorScale * nu.log(1.0 - evenRandoms)
    return randoms

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]/s)\n'
##    myStr += '  x0 = %e\n' % (self.priorStart)
#    myStr += '  s  = %e\n' % (self.priorScale)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorScale, self.priorRange.lo])

  def copy(self):
    return PriorExp(self.priorScale, self.priorRange.lo)

#.......................................................................
class PriorTruncExp(_LnPriorExp):
  def __init__(self, priorScale, lowerBound, upperBound): # We expect this to be called with both lower and upper range bounds defined.
    _LnPriorExp.__init__(self, 'truncExp', priorScale, ra.SimpleRange(lowerBound, upperBound))
    denom = 1.0 - math.exp(-(self.priorRange.hi-self.priorRange.lo)/self.priorScale)
    self.priorAmp = 1.0 / self.priorScale / denom
    self.priorLnAmp = math.log(self.priorAmp)

  def priorDistributedRandoms(self, size=1):
    scale = 1.0 - nu.exp((self.priorRange.lo - self.priorRange.hi) / self.priorScale)
    evenRandoms = nu.random.random(size)
    randoms = self.priorRange.lo - self.priorScale * nu.log(1.0 - scale*evenRandoms)
    return randoms

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = exp(-[x-x0]/s)\n'
##    myStr += '  x0 = %e\n' % (self.priorStart)
#    myStr += '  s  = %e\n' % (self.priorScale)
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__()
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorScale, self.priorRange.lo, self.priorRange.hi])

  def copy(self):
    return PriorTruncExp(self.priorScale, self.priorRange.lo, self.priorRange.hi)

#.......................................................................
class PriorRayleigh(_LnPriorSeparable):
  def __init__(self, priorSigma):
    _LnPriorSeparable.__init__(self, 'rayleigh')
    self.priorSigma = priorSigma

    # Integrating a Rayleigh function yields
    #
    #	    inf
    #	    /         (   -x^2    )
    #	I = | dx x exp(-----------)
    #	    /         ( 2*sig*sig )
    #	   0
    #
    #	          inf
    #	          /
    #	  = sig^2 | du 2*u*e^{-u^2}
    #	          /
    #	         0
    #
    #	  = sig^2.

    self.priorAmp = 1.0 / self.priorSigma / self.priorSigma
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    if x <= 0.0:
      return None
    arg = x / self.priorSigma
    return self.priorLnAmp - arg*arg/2.0 + math.log(x)

  def calcDerivOfLn(self, x):
    if x <= 0.0:
      return None
    return -x / self.priorSigma / self.priorSigma + 1.0 / x

  def calc2ndDerivOfLn(self, x):
    if x <= 0.0:
      return None
    return -1.0 / self.priorSigma / self.priorSigma - 1.0 / x / x

  def priorDistributedRandoms(self, size=1):
    randoms = nu.random.rayleigh(scale=self.priorSigma, size=size)
    return randoms

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = x*exp(-x^2 / [2*s^2])\n'
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    return myStr + '>'

  def getInfo(self):
    return nu.array([self.priorSigma])

  def copy(self):
    return PriorRayleigh(self.priorSigma)

#.......................................................................
class PriorLogRayleigh(_LnPriorSeparable):
  """
The Rayleigh distribution is given by

	            x        (  -x^2 )
	p(x) dx = ----- * exp(-------) dx.
	           s^2       ( 2*s^2 )

If we have x values distributed accordingly, and do a change of variable y = ln(x), the ys are distributed according to

	           e^2y       ( -e^2y )
	p(y) dy = ------ * exp(-------) dy.
	           s^2        ( 2*s^2 )
  """
  def __init__(self, priorSigma):
    _LnPriorSeparable.__init__(self, 'logRayleigh')
    self.priorSigma = priorSigma

    self.priorAmp = 1.0 / self.priorSigma / self.priorSigma
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    return self.priorLnAmp + 2.0*x - math.exp(2.0*x)/2.0/self.priorSigma/self.priorSigma

  def calcDerivOfLn(self, x):
    return 2.0 - math.exp(2.0*x)/self.priorSigma/self.priorSigma

  def calc2ndDerivOfLn(self, x):
    return -2.0*math.exp(2.0*x)/self.priorSigma/self.priorSigma

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = x*exp(-x^2 / [2*s^2])\n'
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    return myStr + '>'
  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Sigma: %r\n' % (self.priorSigma)
    myStr += spaces+'>\n'
    return myStr

  def getInfo(self):
    return nu.array([self.priorSigma])

  def copy(self):
    return PriorLogRayleigh(self.priorSigma)

#.......................................................................
class PriorBurr12C2(_LnPriorSeparable):
  """
The so-called Burr XII aka Singh-Maddala distribution is given by

	          c*k*(x/s)^{c-1}
	p(x) = ---------------------.
	        (1 + [x/s]^c)^{1+k}

If we fix c==2 this becomes

	        2*k              x
	p(x) = ----- * ---------------------.
	         s      (1 + [x/s]^2)^{1+k}

This reaches a maximum where

	           s
	x = ---------------.
	     sqrt(1 + 2*k)

If we define this point as sigma, then of course

	s = sigma * sqrt(1 + 2*k).

For large values of k, this distribution starts to look like the Rayleigh.
  """
  def __init__(self, priorSigma, k):
    _LnPriorSeparable.__init__(self, 'burr12c2')
    self.priorSigma = priorSigma
    self.k = k

    self.s = self.priorSigma * math.sqrt(1.0 + 2.0*self.k)
    self.onePlusK = 1.0 + self.k

    self.priorAmp = 2.0 * self.k / self.s
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    if x <= 0.0:
      return None
    u = x / self.s
    return self.priorLnAmp + math.log(x) - self.onePlusK * math.log(1.0 + u*u)

  def calcDerivOfLn(self, x):
    if x <= 0.0:
      return None
    u = x / self.s
    u2 = u * u
    return (1.0 / x) * (1.0 - self.onePlusK * 2.0 * u2 / (1.0 + u2))

  def calc2ndDerivOfLn(self, x):
    if x <= 0.0:
      return None
    u = x / self.s
    u2 = u * u
    bracket = 1.0 - 2.0*u2/(1.0 + u2)
    wrtU = -1.0/u2 - 2.0*self.onePlusK*bracket/(1.0 + u2)

    return wrtU / self.s / self.s

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = x*exp(-x^2 / [2*s^2])\n'
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    return myStr + '>'

  def getInfo(self):
    return nu.array([self.priorSigma, self.k])

  def copy(self):
    return PriorBurr12C2(self.priorSigma, self.k)

#.......................................................................
class PriorLogBurr12C2(_LnPriorSeparable):
  """
The Burr XII with c fixed at 2 is

	           2*k              x
	p(x) dx = ----- * --------------------- dx.
	            s      (1 + [x/s]^2)^{1+k}

If we have x values distributed accordingly, and do a change of variable y = ln(x), the ys are distributed according to

	           2*k             e^2y
	p(y) dy = ----- * ---------------------- dy.
	            s      (1 + e^2y/s^2)^{1+k}
  """
  def __init__(self, priorSigma, k):
    _LnPriorSeparable.__init__(self, 'logBurr12c2')
    self.priorSigma = priorSigma
    self.k          = k

    self.s = self.priorSigma * math.sqrt(1.0 + 2.0*self.k)
    self.onePlusK = 1.0 + self.k

    self.priorAmp = 2.0 * self.k / self.s
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
#    print 'priors.py line 1011'
#    print '  >> self.priorLnAmp, self.onePlusK, self.s, x:', self.priorLnAmp, self.onePlusK, self.s, x
    try:
      return self.priorLnAmp + 2.0*x - self.onePlusK * math.log(1.0 + math.exp(2.0*x)/self.s/self.s)
    except OverflowError:
      return None

  def calcDerivOfLn(self, x):
    e2xOnS2 = math.exp(2.0*x)/self.s/self.s
    return 2.0 - 2.0 * self.onePlusK * e2xOnS2 / (1.0 + e2xOnS2)

  def calc2ndDerivOfLn(self, x):
    e2xOnS2 = math.exp(2.0*x)/self.s/self.s
    term = e2xOnS2 / (1.0 + e2xOnS2)
    return 4.0 * self.onePlusK * term * (1.0 - term)

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = x*exp(-x^2 / [2*s^2])\n'
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    return myStr + '>'
  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Sigma: %e\n' % (self.priorSigma)
    myStr += spaces+'       K: %e\n' % (self.k)
    myStr += spaces+'>\n'
    return myStr

  def getInfo(self):
    return nu.array([self.priorSigma, self.k])

  def copy(self):
    return PriorLogBurr12C2(self.priorSigma, self.k)

#.......................................................................
class PriorTopHat(_LnPriorSeparable):
  def __init__(self, lowerBound, upperBound):
    _LnPriorSeparable.__init__(self, 'topHat')
    self.priorRange = ra.SimpleRange(lowerBound, upperBound)
    self.priorAmp = 1.0 / (self.priorRange.hi - self.priorRange.lo)
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    if not self.priorRange.contains(x):
      return None
    return self.priorLnAmp

  def calcDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return 0.0

  def calc2ndDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return 0.0

  def priorDistributedRandoms(self, size=1):
    randoms = nu.random.rand(size)
    scaledRandoms = (1.0 - randoms) * self.priorRange.lo + (1.0 - (1.0 - randoms)) * self.priorRange.hi
#    print scaledRandoms
#    print scaledRandoms.shape
    if size<=1:
      return scaledRandoms[0]
    else:
      return scaledRandoms

  def _unflatten(self, flatParValue):
#    if flatParValue<0.0 or flatParValue>=1.0: return None############### put this in superclass!
    return mu.fracVal(self.priorRange.lo, self.priorRange.hi, flatParValue)

#  def __str__(self, spaces=''):
#    myStr  = spaces+'<%s object.\n' % (self.__class__.__name__)
#    myStr += spaces+'   Range: '+self.priorRange.__repr__(spaces=spaces+'  ')+'\n'
#    return myStr + spaces+'>'
  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Range: %r\n' % (self.priorRange)
    myStr += spaces+'>\n'
    return myStr


#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior =1 for lo<x<hi, =0 else.\n'
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__(self)
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorRange.lo, self.priorRange.hi])

  def copy(self):
#    return PriorTopHat(self.priorRange.copy())
    return PriorTopHat(self.priorRange.lo, self.priorRange.hi)

#.......................................................................
class PriorTopHat_20140130(_LnPriorSeparable):
  def __init__(self, priorRange):
    _LnPriorSeparable.__init__(self, 'topHat')
    self.priorRange = priorRange
    self.priorAmp = 1.0 / (priorRange.hi - priorRange.lo)
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    if not self.priorRange.contains(x):
      return None
    return self.priorLnAmp

  def calcDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return 0.0

  def calc2ndDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return 0.0

  def priorDistributedRandoms(self, size=1):
    randoms = nu.random.rand(size)
    scaledRandoms = (1.0 - randoms) * self.priorRange.lo + (1.0 - (1.0 - randoms)) * self.priorRange.hi
#    print scaledRandoms
#    print scaledRandoms.shape
    if size<=1:
      return scaledRandoms[0]
    else:
      return scaledRandoms

  def _unflatten(self, flatParValue):
    return mu.fracVal(self.priorRange.lo, self.priorRange.hi, flatParValue)

#  def __str__(self, spaces=''):
#    myStr  = spaces+'<%s object.\n' % (self.__class__.__name__)
#    myStr += spaces+'   Range: '+self.priorRange.__repr__(spaces=spaces+'  ')+'\n'
#    return myStr + spaces+'>'
  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Range: %r\n' % (self.priorRange)
    myStr += spaces+'>\n'
    return myStr


#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior =1 for lo<x<hi, =0 else.\n'
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__(self)
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorRange.lo, self.priorRange.hi])

  def copy(self):
    return PriorTopHat_20140130(self.priorRange.copy())

#.......................................................................
class PriorPiecewisePower(_LnPriorSeparable):
  """This type of prior is assumed to be valid over the range [0,inf]. That range is broken into 2 or more sections."""
  def __init__(self, priorPowerLo, priorPowerHi, priorKinkXs, priorKinkYs):
    _LnPriorSeparable.__init__(self, 'piecePower')
    self.distObject = rna.PiecewisePowerRandoms(priorPowerLo, priorPowerHi, priorKinkXs, priorKinkYs)

  def calcLnPrior(self, value):
    if value <= 0.0:
      return None
    return self.distObject.lnPdf(value)

  def priorDistributedRandoms(self, size=1):
    return self.distObject.getRandoms(size)

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = y_i*(x/x_i)**(ln[y_{i+1}-y_i]/ln[x_{i+1}-x_i]) for i in [1,n],\n'
#    myStr += '                     = y_1*(x/x_1)**p_i for i=0,\n'
#    myStr += '                     = y_n*(x/x_n)**p_i for i=n+1.\n'
#    myStr += '  p_0 = %e\n' % (self.distObject.powers[0])
#    myStr += '  p_%d = %e\n' % (self.distObject.numKinks+1, self.distObject.powers[-1])
#    for i in range(self.distObject.numKinks):
#      myStr += '  (x,y)_%d = (%e,%e)\n' % (i+1, self.distObject.kinkXs[i], self.distObject.kinkYs[i])
#    return myStr + '>'

  def copy(self):
    return PriorPiecewisePower(priorPowerLo, priorPowerHi, priorKinkXs.copy(), priorKinkYs.copy())########################

#.......................................................................
class PriorPiecewiseExp(_LnPriorSeparable):
  """This type of prior is assumed to be valid over the range [0,inf]. That range is broken into 2 or more sections.

NOTE! If there is a random variate X which obeys a piecewise-power law, log10(X) obeys a piecewise-exponential law with translations as follows:

	priorKLo = (priorPowerLo + 1) * ln(10)
	priorKHi = (priorPowerHi + 1) * ln(10)
	priorKinkXs_exp = log10(priorKinkXs_power)
	priorKinkYs_exp = priorKinkYs_power * priorKinkXs_power * ln(10).

"""
  def __init__(self, priorKLo, priorKHi, priorKinkXs, priorKinkYs):
    _LnPriorSeparable.__init__(self, 'pieceExp')
    self.distObject = rna.PiecewiseExpRandoms(priorKLo, priorKHi, priorKinkXs, priorKinkYs)

  def calcLnPrior(self, value):
    return self.distObject.lnPdf(value)

  def priorDistributedRandoms(self, size=1):
    return self.distObject.getRandoms(size)

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = y_i*exp([ln[y_{i+1}-y_i]/[x_{i+1}-x_i] * [x-x_i]) for i in [1,n],\n'
#    myStr += '                     = y_1*exp(k_i * [x-x_1]) for i=0,\n'
#    myStr += '                     = y_n*exp(k_i * [x-x_n]) for i=n+1.\n'
#    myStr += '  k_0 = %e\n' % (self.distObject.ks[0])
#    myStr += '  k_%d = %e\n' % (self.distObject.numKinks+1, self.distObject.ks[-1])
#    for i in range(self.distObject.numKinks):
#      myStr += '  (x,y)_%d = (%e,%e)\n' % (i+1, self.distObject.kinkXs[i], self.distObject.kinkYs[i])
#    return myStr + '>'

  def copy(self):
    return PriorPiecewiseExp(priorKLo, priorKHi, priorKinkXs.copy(), priorKinkYs.copy())##########################

#.......................................................................
class PriorDeltaFunction(_LnPriorSeparable):
  def __init__(self, priorCentre):
    _LnPriorSeparable.__init__(self, 'diracDelta')
    self.priorCentre = priorCentre

  def calcLnPrior(self, value):
    return 0.0 # not ideal, but it is better to assume that the method will never be queried for value!=self.priorCentre. We don't want to go down the route of comparing two floats, uh-uh. 

  def priorDistributedRandoms(self, size=1):
    randoms = nu.ones([size], nu.float)
    randoms *= self.priorCentre
    return randoms

  def _unflatten(self, flatParValue):
    return self.priorCentre

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = delta(x-x0)\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    return myStr + '>'
  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Centre: %f\n' % (self.priorCentre)
    myStr += spaces+'>\n'
    return myStr

  def getInfo(self):
    return nu.array([self.priorCentre])

  def copy(self):
    return PriorDeltaFunction(self.priorCentre)

#.......................................................................
class PriorLorentzian(_LnPriorSeparable):
  def __init__(self, priorCentre, priorSigma):
    _LnPriorSeparable.__init__(self, 'lorentz')
    self.priorCentre = priorCentre
    self.priorSigma  = priorSigma
    self.priorAmp = 1.0 / math.pi / priorSigma
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    arg = (x - self.priorCentre) / self.priorSigma
    return self.priorLnAmp - math.log(1.0 + arg * arg)

  def calcDerivOfLn(self, x):
    arg = (x - self.priorCentre) / self.priorSigma
    brak = 1.0 + arg * arg
    return -(1.0 / brak) * (2*arg/self.priorSigma)

  def calc2ndDerivOfLn(self, x):
    arg = (x - self.priorCentre) / self.priorSigma
    brak = 1.0 + arg * arg
    return (2.0/brak/self.priorSigma/self.priorSigma)*(2.0*arg*arg/brak - 1.0)

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = 1/(1 + ((x-x0)/s)^2)\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    return myStr + '>'
  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Centre: %r\n' % (self.priorCentre)
    myStr += spaces+'   Sigma: %r\n' % (self.priorSigma)
    myStr += spaces+'>\n'
    return myStr

  def getInfo(self):
    return nu.array([self.priorCentre, self.priorSigma])

  def copy(self):
    return PriorLorentzian(self.priorCentre, self.priorSigma)

#.......................................................................
class PriorJeffreys(_LnPriorSeparable):
  def __init__(self, priorRange):
    _LnPriorSeparable.__init__(self, 'jeffreys')
    self.priorRange = priorRange
    self.priorAmp = 1.0 / (math.log(priorRange.hi) - math.log(priorRange.lo))
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, value):
    if not self.priorRange.contains(value):
      return None
    return self.priorLnAmp - math.log(value)

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior =1/x for lo<x<hi, =0 else.\n'
#    myStr += '  Range of x:\n' % (self.priorRange)
#    myStr += '    '+self.priorRange.__str__(self)
#    return myStr + '\n>'

  def getInfo(self):
    return nu.array([self.priorRange.lo, self.priorRange.hi])

  def copy(self):
    return PriorJeffreys(self.priorRange.copy())

#.......................................................................
class _LnPriorImproper(_LnPriorSeparable):
# We can't easily subsume this into topHat because if only 1 bound is given in a file description of the prior, how do you know if it is upper or lower?

  def __init__(self, typeStr, priorRange):
    _LnPriorSeparable.__init__(self, typeStr)
    self.priorRange = priorRange
    self.priorAmp = 1.0
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
#    print 'xxxx', x
    if self.priorRange.contains(x):
      return self.priorLnAmp
    else:
      return None

  def calcDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return 0.0

  def calc2ndDerivOfLn(self, x):
    if not self.priorRange.contains(x):
      return None
    return 0.0

  def priorDistributedRandoms(self, size=1):
    return None # that's why it is 'improper'.

  def _unflatten(self, flatParValue):
    raise 'cannot unflatten an improper prior'

  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Range: %r\n' % (self.priorRange)
    myStr += spaces+'>\n'
    return myStr

#.......................................................................
class PriorImproper(_LnPriorImproper):
  def __init__(self):
    _LnPriorImproper.__init__(self, 'improper', ra.SimpleRange())

  def getInfo(self):
    return nu.array([])

  def copy(self):
    return PriorImproper()

#.......................................................................
class PriorImproperLo(_LnPriorImproper):
  def __init__(self, lowerBound):
    _LnPriorImproper.__init__(self, 'improperLo', ra.SimpleRange(lowerBound, None))
    self._lowerBound = lowerBound

  def getInfo(self):
    return nu.array([self._lowerBound])

  def copy(self):
    return PriorImproperLo(self._lowerBound)

#.......................................................................
class PriorImproperHi(_LnPriorImproper):
  def __init__(self, upperBound):
    _LnPriorImproper.__init__(self, 'improperHi', ra.SimpleRange(None, upperBound))
    self._upperBound = upperBound

  def getInfo(self):
    return nu.array([self._upperBound])

  def copy(self):
    return PriorImproperHi(self._upperBound)

#.......................................................................
class PriorSine(_LnPriorSeparable):
  def __init__(self, lowerBound, upperBound):
    _LnPriorSeparable.__init__(self, 'sine')
    self.lowerBound = lowerBound
    self.upperBound = upperBound
    self._priorRange = ra.SimpleRange(self.lowerBound, self.upperBound)
    self._scale = (self.upperBound - self.lowerBound) / math.pi
    self.priorAmp = 0.5 / self._scale
    self.priorLnAmp = math.log(self.priorAmp)

  def calcLnPrior(self, x):
    if x <= self.lowerBound or x >= self.upperBound:
      return None
    arg = (x - self.lowerBound) / self._scale
    return self.priorLnAmp + math.log(math.sin(arg))

  def calcDerivOfLn(self, x):
    if x <= self.lowerBound or x >= self.upperBound:
      return None
    arg = (x - self.lowerBound) / self._scale
    return -1.0 / math.tan(arg) / self._scale

  def calc2ndDerivOfLn(self, x):
    if x <= self.lowerBound or x >= self.upperBound:
      return None
    arg = (x - self.lowerBound) / self._scale
    mytan = math.tan(arg)
    return (1.0 + 1.0 / mytan / mytan) / self._scale

  def priorDistributedRandoms(self, size=1):
    raise ex.NotYetImplemented()

  def _unflatten(self, flatParValue):
    raise ex.NotYetImplemented()

#  def __str__(self):
#    myStr  = _LnPriorSeparable.__str__(self)
#    myStr += '  Unnormalized prior = 1/(1 + ((x-x0)/s)^2)\n'
#    myStr += '  x0 = %e\n' % (self.priorCentre)
#    myStr += '  s  = %e\n' % (self.priorSigma)
#    return myStr + '>'
  def __str__(self, spaces=''):
    myStr  = spaces+'<%s.%s instance.\n' % (_module_name, self.__class__.__name__)
    myStr += spaces+'   Range: %r\n' % (self._priorRange)
    myStr += spaces+'>\n'
    return myStr

  def getInfo(self):
    return nu.array([self.lowerBound, self.upperBound])

  def copy(self):
    return PriorSine(self.lowerBound, self.upperBound)

#.......................................................................
def getPrior(priorTypeStr, info):
  if   priorTypeStr=='gauss':
    return PriorGauss(info[0], info[1])

  elif priorTypeStr=='truncGauss':
#    return PriorTruncGauss(  info[0], info[1], ra.SimpleRange(info[2], info[3]))
    return PriorTruncGauss(  info[0], info[1], info[2], info[3])

  elif priorTypeStr=='truncGaussLo':
    return PriorTruncGaussLo(info[0], info[1], info[2])

  elif priorTypeStr=='truncGaussHi':
    return PriorTruncGaussHi(info[0], info[1], info[2])

  elif priorTypeStr=='gamma':
    return PriorGamma(info[0], info[1])

  elif priorTypeStr=='exp':
    return PriorExp(info[0], ra.SimpleRange(info[1], None))

  elif priorTypeStr=='truncExp':
    return PriorTruncExp(info[0], info[1], info[2])

  elif priorTypeStr=='rayleigh':
    return PriorRayleigh(info[0])

  elif priorTypeStr=='logRayleigh':
    return PriorLogRayleigh(info[0])

  elif priorTypeStr=='burr12c2':
    return PriorBurr12C2(info[0], info[1])

  elif priorTypeStr=='logBurr12c2':
    return PriorLogBurr12C2(info[0], info[1])

  elif priorTypeStr=='topHat':
    return PriorTopHat(info[0], info[1])

  elif priorTypeStr=='piecePower':
    raise ex.NotYetImplemented()
    return PriorPiecewisePower(powerLo, powerHi, kinkXs, kinkYs)

  elif priorTypeStr=='pieceExp':
    raise ex.NotYetImplemented()
    return PriorPiecewiseExp(kLo, kHi, kinkXs, kinkYs)

  elif priorTypeStr=='diracDelta':
    return PriorDeltaFunction(info[0])

  elif priorTypeStr=='lorentz':
    return PriorLorentzian(info[0], info[1])

  elif priorTypeStr=='jeffreys':
    return PriorJeffreys(ra.SimpleRange(info[0], info[1]))

  elif priorTypeStr=='improper':
    return PriorImproper()

  elif priorTypeStr=='improperLo':
    return PriorImproperLo(info[0])

  elif priorTypeStr=='improperHi':
    return PriorImproperHi(info[0])

  elif priorTypeStr=='sine':
    return PriorSine(info[0],info[1])

  elif priorTypeStr=='joint':
    raise ex.NotYetImplemented()
    return _LnPriorJoint(indexOfMaster)

  else:
    raise ex.UnrecognizedChoiceObject(priorTypeStr)



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__=='__main__':
  pass
