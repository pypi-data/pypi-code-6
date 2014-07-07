#!/usr/bin/env python

# Name:                         random_aux
#
# Author: Ian Stewart
#
# Functions and classes:
#
#	getExponentialRandom
#	getPowerRandom
#	getRedRandoms
#	getSineRandom
#	getStepRandoms
#	getTruncGaussRandoms
#	PiecewiseExpRandoms
#	PiecewisePowerRandoms
#	PiecewiseRandoms
#	generateRandomString
#
# TODO:
#	- The stuff in _GaussianEnvelopeCoeffs seems to overlap with the functions _gaussianTangentAK() and _gaussianSecantAK() in research/projects/hi_spectra/bayes/stacking/toy_model_3/toy_3_utils.py. Check whether it all can be sucked out and put into maybe math_utils?
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
# History (version, date, change author):
#
#	2014-05-14	IMS/AIfA
#.......................................................................
# * Copied to this release version. Deleted test harness.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_module_name = 'random_aux'

import math
import numpy as nu
from scipy import special

#import ims_exceptions as ex
import local_exceptions as ex
#import SciMathConstants as const
import misc_utils as mu
import math_utils as ma
import fft_aux as fta

_rootTwo = math.sqrt(2.0)
_rootPi  = math.sqrt(math.pi)

#.......................................................................
def generateRandomMask(numBins, numTrueBins):
  if numTrueBins>=numBins:
    return nu.ones([numBins],nu.bool)
  elif numTrueBins<=0:
    return nu.zeros([numBins],nu.bool)

  mask = nu.zeros([numBins],nu.bool)
  numUnsetTrues = numTrueBins
  i = -1
  chance = numUnsetTrues / float(numBins-i-1)
  for i in range(numBins):
    if nu.random.random()<chance:
      mask[i] = True
      numUnsetTrues -= 1
      if numUnsetTrues<=0:
        break

    chance = numUnsetTrues / float(numBins-i-1)

  return mask

#.......................................................................
def getRandomDirection(numDims):
  """
This returns a vector of length numDims which is normalized to length unity. The end of the vector follows a uniform distribution on the surface of a hypersphere of that dimensionality. According to Wolfram Mathworld, the method is described in

Marsaglia, G. "Choosing a Point from the Surface of a Sphere." Ann. Math. Stat. 43, 645-646, 1972.
  """

  vector = nu.random.normal(size=numDims)
  vector /= math.sqrt((vector*vector).sum()) # there is technically some outside chance that the divisor could be zero, but I am not going to bother about it now.
  return vector

#.......................................................................
def getExponentialRandom():
  """Returns a vector of values which have an exponential probability
  ! distribution with a mean value of 1.0."""

#  random = scipy.random.rand()
  evenRandom = nu.random.rand()
  exponentialRandom = -math.log(1.0 - evenRandom) # the subtraction of the
  # random number from 1.0 is to prevent the occurrence of zero- valued
  # argument to log().

  return exponentialRandom

#.......................................................................
class NoCanDoMinus1(Exception): pass

def getPowerRandom(power):
  """
  ! Returns a value which follows a distribution P given by
  ! P(x) = x^power. If power < -1, the distribution is given for for x > 1.0;
  ! if power > -1, the distribution is given for 0 < x <= 1.0. Power==-1 raises an exception.
  """

  oneOverPowerPlusOne = 1.0 / (power + 1.0)
  evenRandom = nu.random.rand()

  if power==-1:
    raise NoCanDoMinus1

  elif power < -1.0:
    powerRandom = (1.0 - evenRandom)**oneOverPowerPlusOne # the subtraction
    # of the random number from 1.0 is to prevent the occurrence of
    # division by zero. 1-rnd may equal 1 but cannot equal 0, hence
    # the taking of negative powers of zero (ie, dividing by zero)
    # is avoided.

  else: # power > -1.0
    powerRandom = evenRandom**oneOverPowerPlusOne

  return powerRandom

#-----------------------------------------------------------------------
def getRedRandoms(requiredNumRandoms, falloffPower=-1.0, padToLowPrimes=True, zeroPadFactor=8):
  """This function returns a vector of numbers which approximate 1/f aka 'red' aka 'brown' noise. Real red noise must have a low-frequency cutoff. This is approximated here simply by setting the 0th channel of the FT of the noise to zero. The returned values are normalized such that their mean=0 and their standard deviation = 1.

It proved to be quite difficult to generate red noise which had the authentic desired power spectrum: some droop at low frequencies and excess power at high seem to be usual. Initially I thought to extend the zero-value at the central frequency by a factor of the zero pad multiple, but I found that this generated unacceptable droop in the first few frequencies. So I have gone back to just setting the zeroth channel value to zero. This however complicates the normalization as seen in the expression in calcRedNoisePower_new().

The results are still not perfect but I am going to accept them for now (2012-03-13).
  """

  paddedSize = fta.findNextHighest2357multiple(requiredNumRandoms) * zeroPadFactor
#  centrePixel = fta.calcFftwRedundantXSize(paddedSize)
  centrePixel = int(paddedSize / 2.0)

  paddedNoise = nu.random.normal(size=paddedSize)
  ftNoise = nu.fft.fft(paddedNoise)

  paddedFilter = nu.zeros([paddedSize], nu.float)
  if falloffPower==-1.0:
    for j in range(1,centrePixel+1):
###    for j in range(zeroPadFactor,centrePixel+1):
      paddedFilter[ j] = 1.0 / float(j)
      paddedFilter[-j] = paddedFilter[j]

  else:
    for j in range(1,centrePixel+1):
###    for j in range(zeroPadFactor,centrePixel+1):
      paddedFilter[ j] = float(j)**falloffPower
      paddedFilter[-j] = paddedFilter[j]

  ftNoise *= paddedFilter
  redNoise = nu.fft.ifft(ftNoise)[:requiredNumRandoms].real
  redNoise -= redNoise.mean()
  stdDev = math.sqrt((redNoise*redNoise).mean())
  redNoise /= stdDev

  return redNoise

#-----------------------------------------------------------------------
def calcRedNoisePower(falloffPower, zeroPadFactor):
  """The function getRedRandoms() returns noise values which have been normalized such that their standard deviation equals unity. The present routine returns the area under the power spectrum of such noise. It is intended to be useful when comparing the power spectrum of simulated noise against theory."""

  return special.zeta(-2.0*falloffPower, zeroPadFactor)

#-----------------------------------------------------------------------
def calcRedNoisePower_new(falloffPower, zeroPadFactor):
  """The function getRedRandoms() returns noise values which have been normalized such that their standard deviation equals unity. The present routine returns the area under the power spectrum of such noise. It is intended to be useful when comparing the power spectrum of simulated noise against theory. Thus a theoretical power spectrum has the functional form

	theory[i] = i**(2.0*falloffPower) * float(len(vector)) / area_new for i>0, =0 else.
  """

  area1 = special.zeta(-2.0*falloffPower, 1.0)
  areaZ = special.zeta(-2.0*falloffPower, float(zeroPadFactor))
  area_new = area1 * area1 / areaZ / float(zeroPadFactor)

  return area_new

#-----------------------------------------------------------------------
class MaxAngleTooBig(ex.OutOfRange):
  def __init__(self, rangeObject, arg):
    self.rangeObject = rangeObject
    self.arg = arg
  def __str__(self):
    return 'Max angle %f was outside the range %s.' % (self.arg, self.rangeObject)

class MinAngleTooSmall(ex.OutOfRange):
  def __init__(self, rangeObject, arg):
    self.rangeObject = rangeObject
    self.arg = arg
  def __str__(self):
    return 'Min angle %f was outside the range %s.' % (self.arg, self.rangeObject)

class NoAngleRange(Exception):
  def __init__(self, minAngle, maxAngle):
    self.minAngle = minAngle
    self.maxAngle = maxAngle
  def __str__(self):
    return 'minAngle %f >= maxAngle %f.' % (self.minAngle, self.maxAngle)

def getSineRandom(maxAngle, minAngle=0.0):
  """
  ! Returns a vector of values which have a distribution P given by
  ! P(x) = sine(x) for 0 <= minX <= x < maxX < Pi. This can be used
  ! to get the radius or codeclination values of points which have a smooth
  ! distribution over a conical segment of a sphere of cone angle maxX radians.

!*** Modified it to avoid trouble at angles near zero, where the random numbers
 in harvest were being squashed into a narrow range just below 1.0 and thus
 losing precision. Should modify it to use sqrt in a small interval close to
 zero. IMS 20060809."""

  if maxAngle > math.pi:
#    raise 'maxAngleTooBig'
    raise MaxAngleTooBig('[0,pi]', maxAngle)
  if minAngle < 0.0:
#    raise 'minAngleTooSmall'
    raise MinAngleTooSmall('[0,pi]', minAngle)
  if minAngle >= maxAngle:
#    raise 'noAngleRange'
    raise NoAngleRange(minAngle, maxAngle)

  c0 = 1.0-math.cos(minAngle)
  c1 = 1.0-math.cos(maxAngle)
  if c0 >= c1:
#    raise 'bug'
    raise ex.Bug('getSineRandom bug')

  return math.acos(1.0-mu.fracVal(c0, c1, nu.random.random()))

#-----------------------------------------------------------------------
def getStepRandoms(binEdges, binHeights, requiredNumRandoms=1, returnBins=False):
  """The returned random has a distribution which is piecewise constant. The values of the 'constants' are given by the N values in 'binHeights'; the intervals within which each constant obtains are given by the N+1 values in 'binEdges'."""

  if not len(binEdges)==len(binHeights)+1:
#    raise 'badLengths'
    raise ex.NonmatchingShapes(len(binEdges), 'binEdges', len(binHeights)+1, 'binHeights')

  numBins = len(binHeights)
  cumulativeEdges = nu.zeros([numBins+1], nu.float)
  for i in range(numBins):
    cumulativeEdges[i+1] = cumulativeEdges[i] + (binEdges[i+1] - binEdges[i]) * binHeights[i]

  integral = cumulativeEdges[numBins]
  cumulativeEdges /= integral

  uniformRandoms = nu.random.random(size=requiredNumRandoms)
  randoms = nu.zeros([requiredNumRandoms], nu.float)
  bins    = nu.zeros([requiredNumRandoms], nu.int)
  i = 0
  for ri in range(requiredNumRandoms):
    i = mu.getBinNumber(cumulativeEdges, uniformRandoms[ri], guessedBinNum=i)
    bins[ri] = i
    randoms[ri] = binEdges[i] + (uniformRandoms[ri] - cumulativeEdges[i]) * integral / binHeights[i]

  if returnBins:
    if requiredNumRandoms>1:
      return (randoms, bins)
    else:
      return (randoms[0], bins[0])
  else:
    if requiredNumRandoms>1:
      return randoms
    else:
      return randoms[0]

#-----------------------------------------------------------------------
class _GaussianEnvelopeCoeffs:
  """This is designed to be used by the rejection method in function getTruncGaussRandoms. If we take logs of all Y values, then an unnormalized Gaussian becomes an inverted parabola with a maximum value of 0. If both low and high truncation intervals are specified, then an envelope function for the parabola in this interval can be found by a series of lines tangent to its surface. In the present case we use a maximum of three lines. One is tangent to the parabola at the lower limit, one at the higher limit, and if the Y value of their interception point is >0, a third line, with slope=0, tangent to the maximum point of the parabola, is added. In 'non-log' coordinates of course the 'straight lines' become exponentials."""

  def __init__(self, sigma, x0, xLo, xHi):
    """In logY coords, the unnormalized Gaussian is given by

	        -(x-x0)^2
	g(x) = -----------
	        2*sigma^2

whereas a generic exponential is

	y(x) = logA + k*x.

An exponential tangent at x=X implies

	y(X) = g(X)
and
	y'(X) = k = g'(X) = -(X-x0)/sigma^2.

From this can be deduced that, for this exponential,

	        2*(X-x0)*X - (X-x0)^2     
	logA = -----------------------
	              2*sigma^2


	        (X-x0)(X+x0)     
	     = --------------.
	         2*sigma^2
    """
    sigmaSquared = sigma * sigma
    logALo = (xLo-x0)*(xLo+x0)/2.0/sigmaSquared
    logAHi = (xHi-x0)*(xHi+x0)/2.0/sigmaSquared
    kLo = (x0-xLo)/sigmaSquared
    kHi = (x0-xHi)/sigmaSquared

    interceptX = (logAHi - logALo) / (kLo - kHi)
    interceptY = logALo + kLo * interceptX

    self.xBounds = [xLo]
    self.logAs = [logALo]
    self.ks = [kLo]
    if interceptY>0.0: # envelope has 3 regions
      self.xBounds.append(-logALo / kLo)
      self.xBounds.append(-logAHi / kHi)
      self.logAs.append(0.0)
      self.ks.append(0.0)

    else: # envelope has just 2 regions
      self.xBounds.append(interceptX)

    self.xBounds.append(xHi)
    self.logAs.append(logAHi)
    self.ks.append(kHi)

    self.envelopeArea = 0.0
    self.cumFracArea = [0.0]
    for i in range(len(self.ks)):
      xLo = self.xBounds[i]
      xHi = self.xBounds[i+1]
      k = self.ks[i]
      logA = self.logAs[i]

      if k==0.0:
        if logA==0.0:
          area = xHi - xLo
        else:
          area = math.exp(logA) * (xHi - xLo)
      else:
        area = math.exp(logA) * (math.exp(k*xHi) - math.exp(k*xLo)) / k

      self.envelopeArea += area
      self.cumFracArea.append(self.envelopeArea)

    for i in range(len(self.cumFracArea)):
      self.cumFracArea[i] /= self.envelopeArea

  def calcBinNum(self, binDecider):
    """To calculate any piecewise random distribution one must first of all decide on which 'piece'. This is done by calculating the cumulative fractional area of the pieces then selecting a piece by seeing where in this cumulative fractional area sequence a uniformly-distributed random number falls. In the present method, the uniform random is presumed to have been chosen and is supplied in the argument binDecider."""
    binNumber = mu.getBinNumber(self.cumFracArea, binDecider)
    return binNumber

  def getTruncExpRandom(self, bin):
    """Returns a random number which is distributed according to an exponential which is truncated between two values."""
    xLo = self.xBounds[bin]
    xHi = self.xBounds[bin+1]
    k = self.ks[bin]
    logA = self.logAs[bin]
    urn = nu.random.random()

    if k==0.0:
      x = urn*xHi + (1.0-urn)*xLo
      if logA==0.0:
#        y = 1.0
        logY = 0.0
      else:
#        y = math.exp(logA)
        logY = logA
    else:
      x = math.log(urn*math.exp(k*xHi) + (1.0-urn)*math.exp(k*xLo)) / k
#      y = math.exp(logA + k*x)
      logY = logA + k*x

#    return (x, y)
    return (x, logY)

  def __call__(self, x):
    if x<self.xBounds[0] or x>self.xBounds[-1]:
      return 0.0

    i = mu.getBinNumber(self.xBounds, x)
    k = self.ks[i]
    logA = self.logAs[i]
    return math.exp(logA + k*x)


def getTruncGaussRandoms(sigma, requiredNumRandoms=1, x0=0.0, xLo=None, xHi=None, style=None):
  """Generates random numbers which follow a distribution which is Gaussian, but truncated on one or both sides. Two basic methods are employed, depending on the value of the 'style' argument, and the values of xLo and xHi. In the one case, gaussian-distributed randoms are generated, those falling outside the truncation interval being rejected; in the other, randoms are generated which follow an envelope distribution comprising piecewise exponentials, then rejection is used to reduce these to the Gaussian."""

  doViaRejection = False # default
  if style=='rejection':
    if xLo==None or xHi==None:
      raise ex.Report("Can't use the rejection method unless both truncation bounds exist.")

    doViaRejection = True
    expCoeffs = _GaussianEnvelopeCoeffs(sigma, x0, xLo, xHi)

  elif style=='simple':
    pass

  elif style==None: # compare areas and decide.
    expCoeffs = _GaussianEnvelopeCoeffs(sigma, x0, xLo, xHi)
    truncGaussArea = ma.integralOfGaussian(sigma, x0, xLo, xHi)
#    normalRatio = truncGaussArea / sigma / const.rootTwo / const.rootPi
    normalRatio = truncGaussArea / sigma / _rootTwo / _rootPi
    rejectRatio = truncGaussArea / expCoeffs.envelopeArea

    if not (xLo==None or xHi==None) and rejectRatio > 5.4*normalRatio: # this ratio comparison is only a rule of thumb since the calculation of a gaussian variate may take a different amount of time to the calculation of an exponential variate. ***The factor of 5.8 reflects the relative speeds of the gaussian vs rejection on my desk top. IMS 20101004.
      doViaRejection = True

  else:
    raise ex.UnrecognizedChoiceObject(style)

  numRandoms = 0
  randoms = []

  if doViaRejection:
    while numRandoms<requiredNumRandoms:
      binDecider = nu.random.random()
      bin = expCoeffs.calcBinNum(binDecider)
      (trialX, logEnvelopeY) = expCoeffs.getTruncExpRandom(bin)
      arg = (trialX - x0) / sigma
      logGaussY = -0.5*arg*arg
      rejectionDecider = nu.random.random()
      if rejectionDecider < math.exp(logGaussY - logEnvelopeY):
        randoms.append(trialX)
        numRandoms += 1

  else: # get Gaussian randoms and throw away any outside the truncation range.
    while numRandoms<requiredNumRandoms:
      trialX = nu.random.normal() * sigma + x0

      if not xLo==None and trialX<xLo:
        continue
      if not xHi==None and trialX>xHi:
        continue

      randoms.append(trialX)
      numRandoms += 1

  if requiredNumRandoms>1:
    return randoms
  else:
    return randoms[0]

#-----------------------------------------------------------------------
class NotIntegrable(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return self.message

class PiecewiseExpRandoms():
  """The PDF in the present case is a sequence of exponentials of the form

	p_i(x) = A * y_i * exp(k_i*[x - x_i]),

for i in [0, N-1]. Each p_i is valid within a range [x_i, x_{i+1}] of x values. There must be at least 2 ranges. For the lowest range, x_i = x_0 = -infinity. The factors k_i should be supplied explicitly for the lowest and highest ranges; for all in-between ranges (if there are any), the factor is calculated from the bounding values (ie the values at the appropriate 'kinks') of x and and y. The number of kinks or nodes is 1 less than the number of ranges, and (since kink 0 is always [-inf, 0]) the first values in the kink arguments represents kink 1 not 0.

Note that kLo = k_0 must be >0, and kHi = k_{N-1} must be <0, for the PDF to be integrable.

The function is defined as a class so the integrals over the intervals need only be calculated once.
  """
  def __init__(self, kLo, kHi, kinkXs, kinkYs):
    self.numKinks  = len(kinkXs)

    if self.numKinks<1:
      raise NotIntegrable('Cannot integrate only 1 segment')
    elif kLo<=0.0:
      raise NotIntegrable('First segment factor must be > 0')
    elif kHi>=0.0:
      raise NotIntegrable('Last segment factor must be < 0')

    # Calculate and store some useful stuff:

    self.kinkXs = kinkXs[:]
    self.kinkYs = kinkYs[:]
    self.kinkLogYs = nu.zeros([self.numKinks], nu.float)
    for i in range(self.numKinks):
      self.kinkLogYs[i] = math.log(kinkYs[i])

    self.ks = nu.zeros([self.numKinks+1], nu.float)
    self.ks[0] = kLo
    for i in range(1,self.numKinks):
      lnY0 = self.kinkLogYs[i-1]
      lnY1 = self.kinkLogYs[i]
      self.ks[i] = (lnY1 - lnY0) / (self.kinkXs[i] - self.kinkXs[i-1])
    self.ks[self.numKinks] = kHi

    # Calculate the segment integrals:
    #
    self.integrals = nu.zeros([self.numKinks+1], nu.float)
    self.betas     = nu.zeros([self.numKinks+1], nu.float)

    i = 0
    y0 = self.kinkYs[i]
    k = self.ks[i]
    self.integrals[i] = y0 / k
    self.betas[i] = y0 / k

    for i in range(1,self.numKinks):
      x0 = self.kinkXs[i-1]
      y0 = self.kinkYs[i-1]
      x1 = self.kinkXs[i]
      k = self.ks[i]
      self.integrals[i] = (y0 / k) * (math.exp(k * (x1 - x0)) - 1.0)
      if k==0.0:
        self.integrals[i] = y0 * (x1 - x0)
        self.betas[i] = y0
      else:
        self.integrals[i] = (y0 / k) * (math.exp(k * (x1 - x0)) - 1.0)
        self.betas[i] = y0 / k

    i = self.numKinks
    y0 = self.kinkYs[i-1]
    k = self.ks[i]
    self.integrals[i] = -y0 / k
    self.betas[i] = y0 / k

    self.amp = 1.0 / self.integrals.sum()
    self.logAmp = math.log(self.amp)

    self.betas *= self.amp

    self.cumSum = nu.zeros([self.numKinks+2], nu.float)
    for i in range(1,self.numKinks+1):
      self.cumSum[i] = self.cumSum[i-1] + self.amp * self.integrals[i-1]
    self.cumSum[self.numKinks+1] = 1.0

  def getRandoms(self, size=1):
    """
For a normalized PDF p(x) the cumulative integral I(x) is defined as follows:

	        x
	       /
	I(x) = | dx p(x).
	       /
	     -inf

Obviously I(-inf) = 0 and I(inf) = 1. To generate a random value with the same distribution as p we need to first generate a random R which is evenly distributed between 0 and 1, then invert the expression for I above to get x = I^-1(R). For the piecewise exponential law, I is given in the ith segment (for all i>0) by

	                         x
	                        /
	I_i(x) = I(x_i) + A*y_i | dx exp(k_i*[x - x_i])
	                        /
	                       x_i

	                   A*y_i
	       = I(x_i) + ------- {exp(k_i*[x - x_i]) - 1},
	                    k_i

where I(x_i) is stored in self.cumSum[i]; A (stored in self.amp) is the constant necessary to normalize the whole PDF integral to 1; and x_i and y_i are respectively the values stored in self.kinkXs[i-1] and self.kinkYs[i-1]. For the 0th segment this expression becomes slightly altered to

	                x
	               /
	I_0(x) = A*y_1 | dx exp(k_0*[x - x_1])
	               /
	              -inf

	          A*y_1
	       = ------- exp(k_0*[x - x_1]).
	           k_0

If we set
	       A*y_i
	B_i = -------
	        k_i
but with
	       A*y_1
	B_0 = -------,
	        k_0

the inverse expressions in terms of the evenly-distributed random R become

	            1    ( R - I[x_i]     )
	x = x_i + -----ln(------------ + 1)
	           k_i   (    B_i         )
and
	            1    (  R  )
	x = x_1 + -----ln(-----).
	           k_0   ( B_0 )

The value of i depends on which range of I the random R falls into. Note that B_i is stored in self.betas[i].

NOTE! In the case that k_i == 0, some of these formulae have to be modified, to wit:

	I_i(x) = I(x_i) + A*y_i * (x - x_i),

thus
	           R - I[x_i]
	x = x_i + ------------
	              B_i
where
	B_i = A*y_i.

NOTE 2! I have used 1-rand rather than rand, since rand can be zero; but this would give an error when calculating randoms for the 0th range. 1-rand can never equal zero so the problem doesn't arise.
"""

    randoms = nu.zeros([size], nu.float)
    evenRandoms = nu.random.random(size)
    for j in range(size):
      evenRandom = 1.0 - evenRandoms[j] # the subtraction of the
      # random number from 1.0 is to prevent the occurrence of zero- valued
      # argument to log().

      # Decide first from which segment to return the random value:
      #
      i = mu.getBinNumber(self.cumSum, evenRandom)
      k = self.ks[i]
      if i<1:
#        randoms[j] = (evenRandoms[j] / self.betas[0])**(1.0/(1.0 + self.powers[0]))
        #             1    (  R  )
        # x = x_1 + -----ln(-----).
        #            k_0   ( B_0 )
        x1 = self.kinkXs[i]
        randoms[j] = x1 + math.log(evenRandom / self.betas[i]) / k
      elif k==0.0:
#        randoms[j] = math.exp((evenRandoms[j] - self.cumSum[i]) / self.betas[i]\
#                       + self.xsToOnePlusQ[i-1])
        #            R - I[x_i]
        # x = x_i + ------------
        #               B_i
        xi = self.kinkXs[i-1]
        randoms[j] = xi + (evenRandom - self.cumSum[i]) / self.betas[i]
      else:
#        randoms[j] = ((evenRandoms[j] - self.cumSum[i]) / self.betas[i]\
#                       + self.xsToOnePlusQ[i-1])**(1.0/(1.0 + self.powers[i]))
        #             1    ( R - I[x_i]     )
        # x = x_i + -----ln(------------ + 1)
        #            k_i   (    B_i         )
        xi = self.kinkXs[i-1]
        randoms[j] = xi + math.log((evenRandom - self.cumSum[i]) / self.betas[i] + 1.0) / k

    return randoms

  def lnPdf(self, x):
    #	p_i(x) = A * y_i * exp(k_i*[x - x_i]),
    # thus
    #	ln(p) = ln(A) + ln(y_i) + k_i*[x - x_i]

#    for i in range(self.numKinks-1,-1,-1): # should give N-1, N-2, ..., 1, 0 for N=self.numKinks.
    for i in range(self.numKinks,0,-1): # should give N, N-1, ..., 2, 1 for N=self.numKinks.
      x0 = self.kinkXs[i-1]
      if x>=x0:
#        lnX0 = self.kinkLogXs[i]
        lnY0 = self.kinkLogYs[i-1]
#        logProb = self.logAmp + lnY0 + self.powers[i] * (math.log(x) - lnX0)
        logProb = self.logAmp + lnY0 + self.ks[i] * (x - x0)
        break

    else:
#      i = self.numKinks
      i = 0
#      lnX0 = self.kinkLogXs[i-1]
      x0 = self.kinkXs[i]
      lnY0 = self.kinkLogYs[i]
#      logProb = self.logAmp + lnY0 + self.powers[i] * (math.log(x) - lnX0)
      logProb = self.logAmp + lnY0 + self.ks[i] * (x - x0)

    return logProb


#-----------------------------------------------------------------------
class PiecewisePowerRandoms():
  """The PDF in the present case is a sequence of power laws of the form

	                     (  x  )^q_i
	p_i(x) = A_i * y_i * (-----),
	                     ( x_i )

for i in [0, N-1]. Each p_i is valid within a range [x_i, x_{i+1}] of x values. There must be at least 2 ranges. For the lowest range, x_i = x_0 = 0; for the highest range, x_i = x_{N-1} = +infinity. The powers q_i should be supplied explicitly for the lowest and highest ranges; for all in-between ranges (if there are any), the power is calculated from the bounding values (ie the values at the appropriate 'kinks') of x and and y.

Note that q_0 must be >-1, and q_{N-1} must be <-1, for the PDF to be integrable.

The function is defined as a class so the integrals over the intervals need only be calculated once.
  """
  def __init__(self, powerLo, powerHi, kinkXs, kinkYs):
    self.numKinks  = len(kinkXs)

    if self.numKinks<1:
      raise NotIntegrable('Cannot integrate only 1 segment')
    elif powerLo<=-1.0:
      raise NotIntegrable('First segment power must be > -1')
    elif powerHi>=-1.0:
      raise NotIntegrable('Last segment power must be < -1')

    # Calculate and store some useful stuff:

    self.kinkXs = kinkXs[:]
    self.kinkYs = kinkYs[:]
    self.kinkLogXs = nu.zeros([self.numKinks], nu.float)
    self.kinkLogYs = nu.zeros([self.numKinks], nu.float)
    for i in range(self.numKinks):
      self.kinkLogXs[i] = math.log(kinkXs[i])
      self.kinkLogYs[i] = math.log(kinkYs[i])

    self.powers = nu.zeros([self.numKinks+1], nu.float)
    self.powers[0] = powerLo
    for i in range(1,self.numKinks):
      lnX0 = self.kinkLogXs[i-1]
      lnY0 = self.kinkLogYs[i-1]
      lnX1 = self.kinkLogXs[i]
      lnY1 = self.kinkLogYs[i]
      self.powers[i] = (lnY1 - lnY0) / (lnX1 - lnX0)
    self.powers[self.numKinks] = powerHi

    self.xsToOnePlusQ = nu.zeros([self.numKinks], nu.float)
    for i in range(self.numKinks):
      if self.powers[i+1]==-1.0:
        self.xsToOnePlusQ[i] = self.kinkLogXs[i]
      else:
        self.xsToOnePlusQ[i] = kinkXs[i]**(1.0 + self.powers[i+1])

    # Calculate the segment integrals:
    #
    self.integrals = nu.zeros([self.numKinks+1], nu.float)
    self.betas     = nu.zeros([self.numKinks+1], nu.float)

    i = 0
    x0 = self.kinkXs[i]
    y0 = self.kinkYs[i]
    power = self.powers[i]
    self.integrals[i] = x0 * y0 / (1.0 + power)
    self.betas[i] = y0 / (1.0 + power) / x0**power

    for i in range(1,self.numKinks):
      x0 = self.kinkXs[i-1]
      y0 = self.kinkYs[i-1]
      x1 = self.kinkXs[i]
      y1 = self.kinkYs[i]
      power = self.powers[i]
      onePlusPower = 1.0 + power

      if onePlusPower==0.0:
        self.integrals[i] = x0 * y0 * (math.log(x1) - math.log(x0))
        self.betas[i] = x0 * y0
      else:
        self.betas[i] = y0 / onePlusPower / x0**power
        self.integrals[i] = self.betas[i] * (x1**onePlusPower - x0**onePlusPower)

    i = self.numKinks
    x0 = self.kinkXs[i-1]
    y0 = self.kinkYs[i-1]
    power = self.powers[i]
#    print i, x0, y0, power
    self.betas[i] = y0 / (1.0 + power) / x0**power
    self.integrals[i] = -self.betas[i] * x0**(1.0 + power)

    self.amp = 1.0 / self.integrals.sum()
    self.logAmp = math.log(self.amp)

    self.betas *= self.amp

    self.cumSum = nu.zeros([self.numKinks+2], nu.float)
    for i in range(1,self.numKinks+1):
      self.cumSum[i] = self.cumSum[i-1] + self.amp * self.integrals[i-1]
    self.cumSum[self.numKinks+1] = 1.0

  def getRandoms(self, size=1):
    """
For a normalized PDF p(x) the cumulative integral I(x) is defined as follows:

	        x
	       /
	I(x) = | dx p(x).
	       /
	     -inf

Obviously I(-inf) = 0 and I(inf) = 1. To generate a random value with the same distribution as p we need to first generate a random R which is evenly distributed between 0 and 1, then invert the expression for I above to get x = I^-1(R). For the piecewise power law, I is given in the ith segment (for all i>0) by

	                             x
	                    A*y_i   /
	I_i(x) = I(x_i) + --------- | dx x^q_i
	                   x_i^q_i  /
	                           x_i

	                        A*y_i
	       = I(x_i) + ----------------- (x^[1+q_i] - x_i^[1+q_i]),
	                   (1+q_i)*x_i^q_i

where I(x_i) is stored in self.cumSum[i]; A (stored in self.amp) is the constant necessary to normalize the whole PDF integral to 1; and x_i and y_i are respectively the values stored in self.kinkXs[i-1] and self.kinkYs[i-1]. For the 0th segment this expression becomes slightly altered to

	                    x
	           A*y_1   /
	I_0(x) = --------- | dx x^q_0
	          x_1^q_0  /
	                  0

	               A*y_1
	       = ----------------- x^[1+q_0].
	          (1+q_0)*x_1^q_0

If we set
	            A*y_i
	B_i = -----------------
	       (1+q_i)*x_i^q_i
but with
	            A*y_1
	B_0 = -----------------,
	       (1+q_0)*x_1^q_0

the inverse expressions in terms of the evenly-distributed random R become

	    ( R - I[x_i]               )^{1/(1+q_i)}
	x = (------------ + x_i^[1+q_i])
	    (    B_i                   )
and
	    (  R  )^{1/(1+q_0)}
	x = (-----).
	    ( B_0 )

The value of i depends on which range of I the random R falls into. Note that B_i is stored in self.betas[i].

NOTE! In the case that q_i == -1, some of these formulae have to be modified, to wit:

	I_i(x) = I(x_i) + A*x_i*y_i * (ln[x] - ln[x_i]),

thus
	       ( R - I[x_i]           )
	x = exp(------------ + ln[x_i])
	       (    B_i               )
where
	B_i = A*x_i*y_i.
"""

    randoms = nu.zeros([size], nu.float)
    evenRandoms = nu.random.random(size)
    for j in range(size):
      # Decide first from which segment to return the random value:
      #
      i = mu.getBinNumber(self.cumSum, evenRandoms[j])
      if i<1:
        randoms[j] = (evenRandoms[j] / self.betas[0])**(1.0/(1.0 + self.powers[0]))
      elif self.powers[i]==-1.0:
        randoms[j] = math.exp((evenRandoms[j] - self.cumSum[i]) / self.betas[i]\
                       + self.xsToOnePlusQ[i-1])
      else:
        randoms[j] = ((evenRandoms[j] - self.cumSum[i]) / self.betas[i]\
                       + self.xsToOnePlusQ[i-1])**(1.0/(1.0 + self.powers[i]))
#      print evenRandoms[j], i, randoms[j]

    return randoms

  def lnPdf(self, x):
    for i in range(self.numKinks):
      if x<self.kinkXs[i]:
        lnX0 = self.kinkLogXs[i]
        lnY0 = self.kinkLogYs[i]
        logProb = self.logAmp + lnY0 + self.powers[i] * (math.log(x) - lnX0)
        break

    else:
      i = self.numKinks
      lnX0 = self.kinkLogXs[i-1]
      lnY0 = self.kinkLogYs[i-1]
      logProb = self.logAmp + lnY0 + self.powers[i] * (math.log(x) - lnX0)

    return logProb


#-----------------------------------------------------------------------
class PiecewiseRandoms():
  """The PDF in the present case is a sequence of N floating-point values P_j.
  """
  def __init__(self, rawProbabilities):
    numValues = len(rawProbabilities)
    self.numValues = numValues
    self.cumSum = nu.zeros([numValues+1], nu.float)
    for i in range(numValues):
      self.cumSum[i+1] = self.cumSum[i] + rawProbabilities[i]

    self.cumSum /= self.cumSum[-1]

  def getRandoms(self, size=1):
    """Returns integers which have the input distribution."""

    randoms = nu.zeros([size], nu.int)
    evenRandoms = nu.random.random(size)
    for j in range(size):
      # Decide first from which segment to return the random value:
      #
      i = mu.getBinNumber(self.cumSum, evenRandoms[j])
      if i<0:
        raise 'PiecewiseRandoms bug 0'
      elif i>self.numValues:
        raise 'PiecewiseRandoms bug 1'
      else:
        randoms[j] = i

    return randoms

#.......................................................................
def generateRandomString(numChars, doLowerCase=False):
  myStr = ''
  intLCA = ord('a')
  if doLowerCase:
    for i in range(numChars):
      myStr += chr(intLCA+int(26*nu.random.random()))

  else:
    intUCA = ord('A')
    for i in range(numChars):
      rndCharInt = int(26*nu.random.random())
      if nu.random.random()>0.5:
        myStr += chr(intUCA+rndCharInt)
      else:
        myStr += chr(intLCA+rndCharInt)

  return myStr

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  pass

