#!/usr/bin/env python

# Name:                         hi_profile
#
# Author: Ian Stewart
#
# TODO:
#	- Figure out the changes needed for an FX correlator.
#	- Is there any neat way to deal with spectra which overlap the edges of the window? In real life these are bandpass-filtered out before correlation (I think).
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
# * Copied to this release version, minus the testbed and using newer model modules.
#
#	2014-05-16	IMS/AIfA
#.......................................................................
# * The nomenclature is now much closer to that of the paper.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
The primary aim of this module is to implement a model for the 21 cm spectral line shape expected from neutral hydrogen in galaxies. See the module testbed.py for examples of how to use it. The theory is described in

	 	arXiv:1405.1838 [astro-ph.IM]

"""

_module_name = 'hi_profile'

import sys
import math
import numpy as nu
from scipy import special

from hiutils import local_exceptions as ex
from hiutils import math_utils as ma
from hiutils import fft_aux as fta
from hiutils import chebyshev as cheb
from hiutils import fitsWcs as wcs
from hiutils import parameter as par
from hiutils import paramz_models as pmod
from hiutils import priors

_twoPi = 2.0 * math.pi
_imaginaryI = 0.0 + 1.0j


#.......................................................................
class HIVanillaParsSpec(par.ParSpecifications):
  """
This is a subclass of paramz_func:ParSpecifications, a class which is intended to contain a variety of information about the parameters of a model. The present class sets up an object of the base type but with the special names appropriate to the HI spectral line model. There are 6 parameters for the line profile, plus whatever extra ones are desired to specify the Chebyshev functions used to model the baseline.

The important difference of the present class over paramz_func:ParSpecifications as far as the HI model is concerned is that two additional attributes are stored: numProfilePars and numChebyOrders.
  """
  _profileParNames = ['lineCentre','lineWidth','totalFlux', 'turbBroadening','fracSolidRotat','asymmetry']
  _profileParFITSNames = ['VCTR','VWID','FLUX','VDISP','FRAC_S','ASYMM']
  _profileParUnits = ['km s^-1',   'km s^-1',  'Jy km s^-1','km s^-1',       '',              '']
  _fluxDensityUnit = 'Jy'
  _xCoordinateUnit = 'm/s'
  numProfilePars = len(_profileParNames)

  def __init__(self, priorsObject=None, parIsPinned=None, profileTransIDs=None, profileExtraTransList=[], numChebyOrders=0, chebyTransform=None):
    """
Explanation of the arguments is as follows:

	- priorsObject: expected to be an object of type priors._LnPriors. In practice, only objects of the subclass priors:LnPriorsSeparable (or perhaps priors:LnPriorsFlat) can be handled. The former type is effectively a list, containing one 'prior' formulation per parameter. There is a library of prior types available in the module priors.py.

	- parIsPinned: a numpy 1D array of booleans. The length should be the same as the number of parameters. If any one of the elements is set True, that is intended as a flag to any fitting routine that that parameter is to be held fixed and not optimized. The default value of None is interpreted as False for each parameter.

	- profileTransIDs: a numpy 1D array of integers. The length should be the same as the number of profile parameters (currently 6). These integers, starting counting at 1, refer to elements of the profileExtraTransList, with zero indicating no transform. The default value of None is interpreted as zero for each parameter.

	- profileExtraTransList: a list object, of no fixed length. Each element is expected to be an object of type parameter:_Transform. What is this all about? It provides machinery to transform some parameters prior to fitting. There are several reasons why this might be desirable. With the HI model for example, it is convenient to transform the line width and the turbulent-broadening parameters by taking their logs. This both makes the fitting of these parameters a little better conditioned, since the distribution of their values among real galaxies seems to be approximately log-normal, and also avoids having to put a sharp bound at zero to prevent non-physical non-positive values of these parameters. To enable this, one should supply profileExtraTransList=[trn.TransformLog10()] and profileTransIDs=nu.array([0,1,0,1,0,0]).

	- numChebyOrders: a scalar integer. What it says.

	- chebyTransform: expected to be an object of type transforms:_Transform. The default value of None is interpreted as no transform.
    """

    if priors==None: # set some which encode the bare physical realities (eg linewidth cannot be -ve).
      if profileTransIDs!=None or chebyTransform!=None:
        raise 'Cannot set priors because you have specified some transforms and I am currently not clever enough to guess best priors for them.'

      listOfSeparablePriors = []
      listOfSeparablePriors.append(priors.PriorImproper())
      listOfSeparablePriors.append(priors.PriorImproperLo(0.0))
      listOfSeparablePriors.append(priors.PriorImproperLo(0.0)) # but flux may be -ve if line is absorbed?
      listOfSeparablePriors.append(priors.PriorImproperLo(0.0))
      listOfSeparablePriors.append(priors.PriorTopHat( 0.0,1.0))
      listOfSeparablePriors.append(priors.PriorTopHat(-1.0,1.0))
      for oi in range(self.numChebyOrders):
        listOfSeparablePriors.append(priors.PriorImproper())
      localPriorsObj = priors.LnPriorsSeparable(listOfSeparablePriors)

    else:
      localPriorsObj = priorsObject

    self._profileTransIDs = profileTransIDs
    self._profileExtraTransList = profileExtraTransList
    self.numChebyOrders = numChebyOrders
    self._chebyTransform = chebyTransform

    parNames = self._profileParNames[:]
    parUnits = self._profileParUnits[:]
    for oi in range(self.numChebyOrders):
      parNames.append('cheby_%d' % (oi))
      parUnits.append('Jy')

    numPars = self.numProfilePars + self.numChebyOrders

    if chebyTransform==None:
      extraTransformsList = profileExtraTransList[:]
      if profileTransIDs==None:
        transformIDs = None
      else:
        transformIDs = nu.zeros([numPars], nu.int)
        transformIDs[:self.numProfilePars] = profileTransIDs.copy()

    else:
      extraTransformsList = profileExtraTransList[:]+[chebyTransform]
      transformIDs = nu.zeros([numPars], nu.int)
      if profileTransIDs!=None:
        transformIDs[:self.numProfilePars] = profileTransIDs.copy()
      transformIDs[self.numProfilePars:numPars] = len(extraTransformsList)

    par.ParSpecifications.__init__(self, parNames, parUnits, parIsPinned\
      , localPriorsObj, transformIDs, extraTransformsList)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def copy(self):
    return HIVanillaParsSpec(self.priors.copy(), self.parIsPinned.copy()\
      , self._profileTransIDs.copy(), self._profileExtraTransList[:]\
      , self.numChebyOrders, self._chebyTransform.copy())

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _strCore(self, spaces=''):
    myStr = par.ParSpecifications._strCore(self, spaces)
    myStr += spaces+'  Number of Chebyshev orders: %d\n' % (self.numChebyOrders)
    return myStr

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def __str__(self, spaces=''):
    me = 'HIVanillaParsSpec'
    myStr = spaces+'<%s.%s instance.\n' % (_module_name, me)
    myStr += self._strCore(spaces)
    myStr += spaces+'>\n'
    return myStr

#.......................................................................
class ChannelDesc:
  """
This class allows one to assign world coordinates (for example Doppler velocity, or radio frequency) to the channels of the output spectrum. Minimal information for this is the worldWCS object which relates these two, plus the number of channels in the output spectrum.

There is a complication which can arise because, in an XF correlator, which HIProfileModel mimics, the spectrum is constructed in lag space (i.e. as the Fourier transform of the spectrum), then converted to frequency channels. The output spectrum may be in different world coordinates (e.g. velocity) and may also not include all of the initial frequency channels.

If the number of frequency channels used by the correlator is known, it can be supplied in the optional argument numFreqChans. If this is not supplied, a value numFreqChans is calculated from numOutputChansRequested by finding the next highest product of small primes. If numFreqChans is supplied, the method looks also for the firstFreqChanOutput argument. In this case also the numOutputChansRequested is compared to the number of frequency channels available, and if it is too large, the actual number of output channels is truncated to the maximum possible value.

The final argument isVelocity is included because we can't work out the relationship between the initial calculation of the spectrum via mimicry of an XF correlator and the desired output coordinates, as recorded in the worldWCS object, without knowing a bit more about the coordinates. If worldWCS._pixelDeltaWorld is positive, isVelocity=True, then the output spectrum will need to be inverted in channel order. If either of those conditions is not true, then no inversion is necessary. I.e. if isVelocity=False it is presumed that the world coordinates are in radio frequency. No other world coordinates are permitted.

Objects of this class are suitable to be supplied to pmod._ParameterizedModel as an rValuesObject. There is no superclass to describe rValues objects (maybe there should be?), hence the absence of inheritance in the present class definition.
  """
  def __init__(self, worldWCS, numOutputChansRequested\
    , numFreqChans=None, firstFreqChanOutput=0, isVelocity=True):

    self.worldWCS                = worldWCS
    self.numOutputChansRequested = numOutputChansRequested

    if numFreqChans==None:
      self.numFreqChans = fta.findNextHighest2357multiple(self.numOutputChansRequested)
    else:
      self.numFreqChans          = numFreqChans

    self.firstFreqChanOutput     = firstFreqChanOutput # may not be <0 - test this?
    self.isVelocity              = isVelocity

    self.channelAbsWidthWorld = abs(worldWCS._pixelDeltaWorld)

    lastFreqChanOutput  = min(self.numFreqChans-1, self.firstFreqChanOutput+self.numOutputChansRequested-1)

    self.numChansOutput = lastFreqChanOutput - self.firstFreqChanOutput + 1

    if (worldWCS._pixelDeltaWorld<0.0  and     self.isVelocity)\
    or (worldWCS._pixelDeltaWorld>=0.0 and not self.isVelocity):
      pixelDeltaWorld =  1.0
      refInWorld = self.firstFreqChanOutput
    else:
      pixelDeltaWorld = -1.0
      refInWorld = lastFreqChanOutput
    self.freqChanWCS = wcs.WCSAxisSimple('FREQCHAN', 1.0, refInWorld, pixelDeltaWorld)

    self.shape = (self.numChansOutput,) # to comply with requirements for the rValuesObject of pmod._ParameterizedModel.

  def getChannelWorldValues(self): # i.e., velocity values.
    # Mainly included as a convenience when plotting a spectrum.
    worldValues = (nu.arange(self.numChansOutput)-(self.worldWCS.refInPixels-1.0))\
      * self.worldWCS._pixelDeltaWorld + self.worldWCS.refInWorld
    return worldValues

#.......................................................................
class SimpleVelChannelDesc(ChannelDesc):
  def __init__(self, velFirstChan, velLastChan, numOutputChans, worldUnit='km/s'):

    channelDelta = (velLastChan - velFirstChan) / float(numOutputChans-1)
    refVel = velFirstChan

    velWCS = wcs.WCSAxisSimple('VELO', 1.0, velFirstChan, channelDelta\
      , worldUnit=worldUnit)

    ChannelDesc.__init__(self, velWCS, numOutputChans)

#.......................................................................
class HIProfileModel(pmod._ParameterizedModel):
  """
The purpose of this class is to return a vector of floating-point values which represent the flux density in janskys of a galactic HI spectral line profile, sampled at a series of recession velocities. The profile model has 6 parameters for the line profile plus some optional extra ones to model the baseline.

The most important method for the user is probably going to be calcModelValues(parValues) (this is inherited here from pmod._ParameterizedModel).
  """
  def __init__(self, hiParsSpecObj, channelDesc, smoothing=None, applyAsymmToSolid=True):
    """
Description of the arguments:

	- hiParsSpecObj: an object of type parameter:ParSpecifications, but which has the additional attributes
		* numProfilePars
		* numChebyOrders
	This object specifies the number of parameters (6 profile ones plus the desired number to fit the baseline), plus any priors or transforms for these. The subclass HIVanillaParsSpec provides a convenient way to specify the parameters; hi_fit:HIParsSpecLogs and hi_fit:SimpleParamInfo are more compact still. Note also that parameters can be specified via a FITS file which is read by hi_fit:readParsFromFITS().

	- channelDesc: an object of type ChannelDesc which describes the number and units of the channels in the output spectrum. The subclass SimpleVelChannelDesc provides a useful short cut.

	- smoothing: a string which specifies the filtering. Anticipated allowed values are:
		None
		'hanning_raw'
		'hanning_sieve'
		'tukey_25'

	- applyAsymmToSolid: a scalar boolean. If True, the asymmetry parameter is applied not only to the flat-rotation part of the profile model but equally to the solid-rotating part.

The spectrum is calculated internally in units of frequency channels - that is, the channel index of the initial spectrum vector increases with frequency. The size of this vector is specified by channelDesc.numFreqChans, which would normally be expected to be a power of 2, or at least a product of low primes.

Since recession velocity is inversely proportional to frequency, the user may wish to invert the order in which the channels of the spectrum vector are returned. This is implemented via channelDesc.freqChanWCS._pixelDeltaWorld: a negative value will cause an order inversion within the method _sliceFromRawToData().

The user may also wish to choose a subset of the channels of the returned spectrum. This is selected via channelDesc.firstFreqChanOutput and channelDesc.numOutputChans.
    """

    self.smoothing          = smoothing
    self.applyAsymmToSolid  = applyAsymmToSolid
    self.channelDesc        = channelDesc

    pmod._ParameterizedModel.__init__(self, hiParsSpecObj, channelDesc)

    if smoothing=='hanning_sieve':
      self.numSamples = 4*self.channelDesc.numFreqChans
    else:
      self.numSamples = 2*self.channelDesc.numFreqChans

    self.centreSample = self.numSamples // 2
    self.dt = 0.5 / float(self.channelDesc.numFreqChans)

    self.j0Values   = None
    self.jincValues = nu.zeros([self.centreSample+1], nu.float)
    self.j1Values   = None
    self.gValues    = None
    self.expiValues = None
    self.eValues    = nu.zeros([self.centreSample+1], nu.float)
    self.filtValues = nu.ones( [self.centreSample+1], nu.float)

    self.ftValues   = nu.zeros([self.numSamples], nu.complex)

    self.halfChanFracs = nu.arange(self.centreSample+1) * self.dt

    if smoothing==None:
      pass

    elif smoothing=='hanning_raw' or smoothing=='hanning_sieve':
      angles = (nu.arange(self.centreSample+1) / float(self.numSamples)) * _twoPi
      self.filtValues = 0.5*(1.0 + nu.cos(angles))

    elif smoothing=='tukey_25':
      # The Tukey filter function is a cyclic repetition of the following function defined in the range 0<=f<1:
      # 
      # 	G(f) = 1 for 0 <= f < a/2 or 1-a/2 <= f < 1,
      # 
      # 	     = 0.5*{1 + cos(2*pi*[f-a/2]/[1-a])} for a/2 <= f < 1-a/2.
      # 
      # The number here given as 'a' is the input argument 'aFraction'. Obviously it must be in the range 0 to 1. Note however that a value of exactly 1 will cause the function to fail.

      aFraction = 0.25 # *************** should put the actual routine below in a separate, generic function.

      for i in range(1, self.centreSample+1):
        cyclicF = i / float(self.numSamples) # cycle repeats when this is an exact multiple of 1.
        f = cyclicF % 1.0
        if f<aFraction/2.0 or f>=1.0-aFraction/2.0:
          self.filtValues[i] = 1.0
        else:
          angle = 2.0 * math.pi * (f - aFraction/2.0) / (1.0 - aFraction)
          self.filtValues[i] = 0.5*(1.0 + math.cos(angle))

    else:
      raise ex.UnrecognizedChoiceObject(smoothing)

    self.chebyshevs = cheb.generateChebyshevSamples(self.channelDesc.numChansOutput, self.parsSpecObj.numChebyOrders)

  #.....................................................................
  def _readPars(self, parValues):
    # Model parameters are converted here from the given world coordinates to frequency channels.

    lineCentreWorld     = parValues[0]	# v0
    halfLineWidthWorld  = parValues[1]/2.0	# Dv
    totalFluxWorld      = parValues[2]	# A
    turbBroadSigmaWorld = parValues[3]	# s
    f                   = parValues[4]	# f
    asymmetry          = parValues[5]	# B
    # If there are any more, they are Chebyshev baseline coefficients which we read directly from parValues.

    lineCentreOutChan = self.channelDesc.worldWCS.worldToPixel(lineCentreWorld)-1.0
    lineCentreDeltaFChan = self.channelDesc.freqChanWCS.pixelToWorld(lineCentreOutChan+1.0)
    halfLineWidthFChan   = halfLineWidthWorld  / self.channelDesc.channelAbsWidthWorld
    totalFluxFChan       = totalFluxWorld      / self.channelDesc.channelAbsWidthWorld
    turbBroadSigmaFChan  = turbBroadSigmaWorld / self.channelDesc.channelAbsWidthWorld

    return (lineCentreDeltaFChan, halfLineWidthFChan, totalFluxFChan, turbBroadSigmaFChan, f, asymmetry)

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcModelValueUntrans(self, parValues, rValue):
    raise ex.EmptyMethod() # There's no easy way to implement this with the present algorithm.

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcModelValuesUntrans(self, parValues):
    """
The line profile model is calculated in this method over a vector of velocity values.

The model has 6 parameters, listed below:

	Symbol in this		Variable name		Notes:
	docstring:		in the code:
------------------------------------------------------------------------
p0	    v0			lineCentre		In km/s.
p1	    Dv			lineWidth		In km/s.
p2	    S			totalFlux		In Jy km/s.
p3	    sigma		turbBroadSigma		Sigma (in km/s) for the Gaussian convolution of the raw line.
p4	    f			f			Fraction of the HI which is 'solid rotating'. Valid range is [0,1].
p5	    alpha		asymmetry		Valid range is -1 to +1. Positive values give a higher horn on the high-velocity side.
------------------------------------------------------------------------

The full formula for the Fourier-transformed line profile Z(tau) (not considering here the baseline) is

	Z(tau) = Z_intr(tau) * G(tau)

where Z_intr(tau) is the intrinsic, undispersed profile and G(tau) is the transform of the dispersive convolver (therefore also a Gaussian). These in turn are given by

	                                   [{                 2*f         }
	Z_intr(tau) = 2*S*exp(i*psi*tau) * [{(1-f)*J0(tau) + -----*J1(tau)} +
	                                   [{                 tau         }

	                                                    ]
	            + i*alpha * {(1-f)*J1(tau) + 2*f*E(tau)}]
	                                                    ]
and
	            [   ( sigma     )^2]
	G(tau) = exp[-2*(-------*tau)  ].
	            [   (   w       )  ]

In the expression for Z_intr(tau), E(tau) is shorthand for

	           1     [  2                    ]
	E(tau) = ----- * [-----*J1(tau) - J0(tau)].
	          tau    [ tau                   ]

There are many variables here, so I'll go through the above expressions in order and explain them one by one. (I omit the 6 model parameters, already defined above.)

	          pi * Dv
	tau = ----------------.
	       2 * N_chan * w

	       2*(v_hi - v0)
	psi = ---------------.
	            Dv

	J0, J1: Bessel functions of the first kind, of order 0 and 1.

	w: the channel width in km/s (absolute value of the channel delta v).

	N_chan: number of spectral channels.

	v_hi: the highest velocity of the spectrum.

    """
    (lineCentreF, halfLineWidthF, totalFluxF, turbBroadSigmaF, f, asymmetry) = self._readPars(parValues)

    # Now calculate the FTs of all profile components:
    #
    dTauBy2N     = _twoPi * halfLineWidthF
    dTauOnPiBy2N = 2.0 * halfLineWidthF
    psiDTauBy2N  = -_twoPi * lineCentreF
    gaussArgBy2N = math.pi * turbBroadSigmaF

    taus      = dTauBy2N     * self.halfChanFracs
    psiTaus   = psiDTauBy2N  * self.halfChanFracs
    gaussArgs = gaussArgBy2N * self.halfChanFracs
    tausOnPi  = dTauOnPiBy2N * self.halfChanFracs

    self.j0Values = special.j0(taus)
    self.j1Values = special.j1(taus)
    self.expiValues = nu.cos(psiTaus) + _imaginaryI * nu.sin(psiTaus)
    self.gValues = nu.exp(-2.0 * gaussArgs * gaussArgs)

    #
    #	jinc(x) = J1(pi*x)/2/x. Use series expansion for small x.
    #
    if halfLineWidthF>0.0:
      tBoundary = ((3.0*64.0*ma.precision)**0.25) / dTauBy2N
      tiFinis = 1+int(tBoundary/self.dt)
      if tiFinis<self.centreSample:
        tempValues = self.halfChanFracs[:tiFinis] * self.halfChanFracs[:tiFinis] * dTauBy2N * dTauBy2N / 8.0
        self.jincValues[:tiFinis] = 0.25 * math.pi * (1.0 - tempValues)
        self.jincValues[tiFinis:] = self.j1Values[tiFinis:] / 2.0 / tausOnPi[tiFinis:]
      else:
        tempValues = taus * taus / 8.0
        self.jincValues = 0.25 * math.pi * (1.0 - tempValues)
    else:
      self.jincValues += 0.25 * math.pi

    # E as a whole is well behaved near tau==0, but the two Bessel terms individually each have a singularity there. The Taylor-series expansion of the Bessel function of order k about zero is
    #	        __
    #	        \         (-1)^j       ( x )^{2*j+k}
    #	Jk(x) =  >     ------------- * (---).
    #	        /_j=0   j! * (j+k)!    ( 2 )
    #
    # For this we can derive the following expansion for E(tau) as tau->0:
    #	         __
    #	         \        (-1)^j       ( tau )^{2*j+1}
    #	E(tau) =  >    ------------- * (-----).
    #	         /_j=0  2*j!*(j+2)!    (  2  )
    #
    #	       [ tau     tau^3            ]    tau  [      tau^2            ]
    #	     = [----- - ------- + O(tau^5)] = -----*[ 1 - ------- + O(tau^4)].
    #	       [  8       96              ]     8   [       12              ]
    #
    # The first term alone is a good approximation provided tau^2 < 12*precision.
    #
    if self.applyAsymmToSolid:
      if halfLineWidthF>0.0:
        tBoundary = math.sqrt(12.0*ma.precision) / dTauBy2N
        tiFinis = 1+int(tBoundary/self.dt)
        if tiFinis<self.centreSample:
          self.eValues[:tiFinis] = taus[:tiFinis]/8.0
          self.eValues[tiFinis:] = ((4.0/math.pi)*self.jincValues[tiFinis:]\
            - self.j0Values[tiFinis:]) / taus[tiFinis:]
        else:
          self.eValues = taus / 8.0
      else:
        self.eValues = nu.zeros([self.centreSample+1], nu.float)

    else:
      self.eValues *= 0.0

    zintrValues = (1.0-f)*self.j0Values + (4.0*f/math.pi) * self.jincValues\
      + _imaginaryI * asymmetry * ((1.0-f)*self.j1Values + 2.0*f*self.eValues)

    zintrValues *= 2.0 * totalFluxF * self.expiValues

    self.ftValues[:self.centreSample+1] = zintrValues * self.gValues * self.filtValues

    # Copy over conjugate values into the other half of the array, then back transform, finally rebin:
    #
    self.ftValues = fta.doHermitianCopy(self.ftValues, nullifyCentralImaginary=True)

    modelValues = self._transformAndChunk(self.ftValues)

    # Add in the baseline. *** NOTE *** that this is done AFTER the inversion of the channel order if increasing velocity order is desired. Changing the sign of the channel delta V will therefore invert the profile but will not affect the baseline.
    #
    for oi in range(self.parsSpecObj.numChebyOrders):
      modelValues += self.chebyshevs[:,oi] * parValues[oi+self.parsSpecObj.numProfilePars]

    return modelValues

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _transformAndChunk(self, ftValues):
    if self.smoothing=='hanning_sieve':
      rawSpectrum = (nu.fft.fft(ftValues.real).real / float(self.numSamples))[0:2*self.channelDesc.numFreqChans:2] * 2.0
    else:
      rawSpectrum = (nu.fft.fft(ftValues.real).real / float(self.numSamples))[0:self.channelDesc.numFreqChans]

    spectrum = self._sliceFromRawToData(rawSpectrum)

    return spectrum

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _sliceFromRawToData(self, rawVector):
    lastFreqChanOutput = self.channelDesc.firstFreqChanOutput + self.channelDesc.numChansOutput - 1
    if self.channelDesc.freqChanWCS._pixelDeltaWorld < 0.0:
      tempVector = rawVector[self.channelDesc.firstFreqChanOutput:lastFreqChanOutput+1]
      return tempVector[::-1] # velocities run from low to high in the returned vector.
    else:
      return rawVector[self.channelDesc.firstFreqChanOutput:lastFreqChanOutput+1] # this matches a data set with the velocities going from high to low (such as the THINGS cubes).

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcEDerivs(self, df, dTauBy2N):
    #		{tau*E'} = 3*J0(tau)/tau + (1-6/tau)*J1(tau)/tau
    #		      = {3*J0(tau) - (12/pi)*jinc(tau/pi)}/tau + J1(tau)
    #		      = J1(tau) - 3*E(tau).
    #
    # {tau*E'} as a whole is well behaved near tau==0, but the two terms individually each have a singularity there. The following expansion can be used near zero:
    #		                __
    #		                \      (2*j+1)*(-1)^j    ( tau )^{2*j+1}
    #		{tau*E'}(tau) =  >    ---------------- * (-----)
    #		                /_j=0    2*j!*(j+2)!     (  2  )
    #
    #		           [ tau     tau^3            ]    tau  [      tau^2            ]
    #		         = [----- - ------- + O(tau^5)] = -----*[ 1 - ------- + O(tau^4)].
    #		           [  8       32              ]     8   [        4              ]
    #
    # The first term alone is a good approximation provided tau^2 < 4*precision.
    #
    eDerivs = nu.zeros([self.centreSample+1], nu.float)
    if self.applyAsymmToSolid:
      if df>0.0:
        tBoundary = math.sqrt(4.0*ma.precision) / dTauBy2N
        tiFinis = 1+int(tBoundary/self.dt)
        if tiFinis<self.centreSample:
          eDerivs[:tiFinis] = dTauBy2N*self.halfChanFracs[:tiFinis]/8.0
          eDerivs[tiFinis:] = self.j1Values[tiFinis:] - 3.0*self.eValues[tiFinis:]
        else:
          eDerivs = dTauBy2N * self.halfChanFracs / 8.0

    return eDerivs

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcDMByDParKUntrans(self, parValues, k, recalcModel=True):
    """
This calculates a vector of derivatives of the model with respect to parameter k, over all N channels, evaluated at the supplied values of the parameters.
    """
    (lineCentreF, halfLineWidthF, totalFluxF, turbBroadSigmaF, f, asymmetry) = self._readPars(parValues)

    if recalcModel:
      self._setModelValuesUntrans(parValues)

    w = self.channelDesc.channelAbsWidthWorld # for short

    if   k==0: # lineCentre
      localFtValues = nu.zeros([self.numSamples], nu.complex)
      localFtValues[:self.centreSample+1] = _twoPi * _imaginaryI * self.halfChanFracs / w
      localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
      localFtValues *= self.ftValues
      derivVector = self._transformAndChunk(localFtValues)

    elif k==1: # lineWidth
      df = halfLineWidthF # for short
      dTauBy2N = _twoPi * df
      taus = dTauBy2N * self.halfChanFracs

      eDerivs = self._calcEDerivs(df, dTauBy2N)

      dZintrValues = (2.0*f + _imaginaryI*asymmetry*taus*(1.0-f))*self.j0Values\
               + (taus + _imaginaryI*asymmetry)*(f-1.0)*self.j1Values\
               + (-8.0*f/math.pi)*self.jincValues\
               + _imaginaryI*asymmetry*2.0*f*eDerivs

      dZintrValues /= (2.0 * w * df)
      dZintrValues *= 2.0 * totalFluxF * self.expiValues

      localFtValues = nu.zeros([self.numSamples], nu.complex)
      localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
      localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
      derivVector = self._transformAndChunk(localFtValues)

    elif k==2: # totalFlux
      derivVector = self.mValues / (totalFluxF * w)

    elif k==3: # turbBroadSigma
      localFtValues = nu.zeros([self.numSamples], nu.complex)
      localFtValues[:self.centreSample+1] = _twoPi * _imaginaryI * self.halfChanFracs / w
      localFtValues *= localFtValues * turbBroadSigmaF * w
      localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
      localFtValues *= self.ftValues
      derivVector = self._transformAndChunk(localFtValues)

    elif k==4: # f
      dZintrValues = -self.j0Values + (4.0/math.pi)*self.jincValues + _imaginaryI*asymmetry*(-self.j1Values + 2.0*self.eValues)
      dZintrValues *= 2.0 * totalFluxF * self.expiValues

      localFtValues = nu.zeros([self.numSamples], nu.complex)
      localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
      localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
      derivVector = self._transformAndChunk(localFtValues)

    elif k==5: # asymmetry
      dZintrValues = _imaginaryI*((1.0-f)*self.j1Values + 2.0*f*self.eValues)
      dZintrValues *= 2.0 * totalFluxF * self.expiValues

      localFtValues = nu.zeros([self.numSamples], nu.complex)
      localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
      localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
      derivVector = self._transformAndChunk(localFtValues)

    else:
      derivVector = self.chebyshevs[:,k-self.parsSpecObj.numProfilePars]

    return derivVector

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  def _calcD2MByDParsKLUntrans(self, parValues, k, l, recalcModel=True):
    """
This calculates a vector of second derivatives of the model with respect to parameters k and l, over all N channels, evaluated at the supplied values of the parameters. Note that it is assumed that l is always >= k.
    """
    (lineCentreF, halfLineWidthF, totalFluxF, turbBroadSigmaF, f, asymmetry) = self._readPars(parValues)

    if recalcModel:
      self._setModelValuesUntrans(parValues)

    w = self.channelDesc.channelAbsWidthWorld # for short
    df = halfLineWidthF # for short
    dTauBy2N = _twoPi * df
    taus = dTauBy2N * self.halfChanFracs

    eDerivs = self._calcEDerivs(df, dTauBy2N)

    derivVector = nu.zeros([self.channelDesc.numChansOutput], nu.float) # the default

    if   k==0: # lineCentre
      if   l==0: # lineCentre
        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = _twoPi * _imaginaryI * self.halfChanFracs / w
        localFtValues *= localFtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        localFtValues *= self.ftValues
        derivVector = self._transformAndChunk(localFtValues)

### Can't do the following unless we extend self.halfChanFracs:
#        derivVector = self._calcDMByDParKTrans(transParValues, 0)
#        derivVector *= _twoPi * _imaginaryI * self.halfChanFracs / self.channelAbsWidthVel

      elif l==1: # lineWidth
        dZintrValues = (2*f + _imaginaryI*asymmetry*taus*(1.0-f))*self.j0Values\
                 - (taus + _imaginaryI*asymmetry)*(1.0-f)*self.j1Values\
                 - (8.0*f/math.pi)*self.jincValues\
                 + _imaginaryI*asymmetry*2.0*f*eDerivs

        dZintrValues *= math.pi * _imaginaryI * self.halfChanFracs / w / w / df # NOTE! This only works provided df > 0.
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

      elif l==2: # totalFlux
        derivVector = self._calcDMByDParKUntrans(parValues, 0) / (totalFluxF * w)

      elif l==3: # turbBroadSigma
        dZintrValues = _twoPi * _imaginaryI * self.halfChanFracs / w

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * dZintrValues * dZintrValues
        localFtValues *= turbBroadSigmaF * w
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        localFtValues *= self.ftValues
        derivVector = self._transformAndChunk(localFtValues)

      elif l==4: # f
        dZintrValues = -self.j0Values + (4.0/math.pi)*self.jincValues\
                 + _imaginaryI*asymmetry*(-self.j1Values + 2.0*self.eValues)
        dZintrValues *= _twoPi * _imaginaryI * self.halfChanFracs / w
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

      elif l==5: # asymmetry
        dZintrValues = _imaginaryI*((1.0-f)*self.j1Values + 2.0*f*self.eValues)
        dZintrValues *= _twoPi * _imaginaryI * self.halfChanFracs / w
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

    elif k==1: # lineWidth
      if   l==1: # lineWidth
        eDerivs2 = nu.zeros([self.centreSample+1], nu.float)
        if self.applyAsymmToSolid:
          if df>0.0:
            tBoundary = math.sqrt(48.0/5.0*ma.precision) / dTauBy2N
            tiFinis = 1+int(tBoundary/self.dt)
            if tiFinis<self.centreSample:
              eDerivs2[:tiFinis] = -taus[:tiFinis]*taus[:tiFinis]*taus[:tiFinis]/16.0
              eDerivs2[tiFinis:] = (12.0-taus[tiFinis:]*taus[tiFinis:])*self.eValues[tiFinis:] - 3.0*self.j1Values[tiFinis:]
            else:
              eDerivs2 = -taus*taus*taus/16.0

        dZintrValues = ((f-1.0)*taus*(taus + _imaginaryI*asymmetry) - 6.0*f)*self.j0Values\
                 + ((1.0-f)*(taus + _imaginaryI*asymmetry*(2.0-taus*taus)) - 2.0*f*taus)*self.j1Values\
                 + (24.0*f/math.pi)*self.jincValues\
                 + _imaginaryI*asymmetry*2.0*f*eDerivs2

        dZintrValues /= 2.0 * df * w
        dZintrValues /= 2.0 * df * w
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

      elif l==2: # totalFlux
        derivVector = self._calcDMByDParKUntrans(parValues, 1) / (totalFluxF * w)

      elif l==3: # turbBroadSigma
        localFtValues = _twoPi * _imaginaryI * self.halfChanFracs / w

        dZintrValues = (2.0*f + _imaginaryI*asymmetry*taus*(1.0-f))*self.j0Values\
                 + (taus + _imaginaryI*asymmetry)*(f-1.0)*self.j1Values\
                 + (-8.0*f/math.pi)*self.jincValues\
                 + _imaginaryI*asymmetry*2.0*f*eDerivs

        dZintrValues /= (2.0 * w * df)
        dZintrValues *= localFtValues * localFtValues * turbBroadSigmaF * w
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)


      elif l==4: # f
        dZintrValues = (2.0 - _imaginaryI*asymmetry*taus)*self.j0Values\
                 + (taus + _imaginaryI*asymmetry)*self.j1Values\
                 - (8.0/math.pi)*self.jincValues\
                 + 2.0*_imaginaryI*asymmetry*eDerivs
        dZintrValues /= 2.0 * w * df # NOTE! This only works provided df > 0.
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

      elif l==5: # asymmetry
        dZintrValues = (_imaginaryI*taus*(1.0-f))*self.j0Values\
                 - (1.0-f)*_imaginaryI*self.j1Values\
                 + _imaginaryI*2.0*f*eDerivs
        dZintrValues /= 2.0 * w * df # NOTE! This only works provided df > 0.
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

    elif k==2: # totalFlux
      if   l==2: # totalFlux
        derivVector = self.mValues * 0.0

      elif l==3: # turbBroadSigma
        derivVector = self._calcDMByDParKUntrans(parValues, 3) / (totalFluxF * w)

      elif l==4: # f
        derivVector = self._calcDMByDParKUntrans(parValues, 4) / (totalFluxF * w)

      elif l==5: # asymmetry
        derivVector = self._calcDMByDParKUntrans(parValues, 5) / (totalFluxF * w)

    elif k==3: # turbBroadSigma
      s = turbBroadSigmaF * w

      if   l==3: # turbBroadSigma
        dZintrValues = _twoPi * _imaginaryI * self.halfChanFracs / w
        dZintrValues *= dZintrValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * (dZintrValues * s * s + 1.0)
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        localFtValues *= self.ftValues
        derivVector = self._transformAndChunk(localFtValues)

      elif l==4: # f
        dZintrValues = _twoPi * _imaginaryI * self.halfChanFracs / w
        dZintrValues *= dZintrValues * s
        dZintrValues *= -self.j0Values + (4.0/math.pi)*self.jincValues\
           + _imaginaryI*asymmetry*(-self.j1Values + 2.0*self.eValues)
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

      elif l==5: # asymmetry
        dZintrValues = _twoPi * _imaginaryI * self.halfChanFracs / w
        dZintrValues *= dZintrValues * s
        dZintrValues *= _imaginaryI*((1.0-f)*self.j1Values + 2.0*f*self.eValues)
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

    elif k==4: # f
      if   l==4: # f
        derivVector = self.mValues * 0.0

      elif l==5: # asymmetry
        dZintrValues = _imaginaryI*(-self.j1Values + 2.0*self.eValues)
        dZintrValues *= 2.0 * totalFluxF * self.expiValues

        localFtValues = nu.zeros([self.numSamples], nu.complex)
        localFtValues[:self.centreSample+1] = dZintrValues * self.gValues * self.filtValues
        localFtValues = fta.doHermitianCopy(localFtValues, nullifyCentralImaginary=True)
        derivVector = self._transformAndChunk(localFtValues)

    elif k==5: # asymmetry
      if   l==5: # asymmetry
        derivVector = self.mValues * 0.0

    return derivVector


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__=='__main__':
  pass





