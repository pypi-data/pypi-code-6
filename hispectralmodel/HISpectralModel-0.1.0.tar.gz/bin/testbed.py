#!/usr/bin/env python

# Name:                         testbed
#
# Author: Ian Stewart
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
#	 2014-05-14	IMS/AIfA
#.......................................................................
# + First draft. Carved off from hi_profile.py.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
This is a module for testing the code which constructs the HI line profile. The user should refer for background information about the model to

	 	arXiv:1405.1838 [astro-ph.IM]

Useage:
=======

The user should call the present module as follows (note that prefixing the calls with 'python' is not necessary):

	./testbed.py <style> <filterStyle> <centreVel> <lineWidth> <totalFlux> <turbBroadSigma> <fracSolidRot> <asymmetry> <chebyCoeffsStr> <numChans> <refChan> <refVel> <channelDelta> <additional arguments>

The command-line arguments will be decribed in detail shortly, but first some general notes:

	- All velocity units are assumed to be km/s
	- The unit of total flux is Jy km/s

Command-line arguments:
-----------------------

	style		This may be 'spectrum', 'diff' or 'diff2'. 'spectrum' produces a plot of the line profile; 'diff' a plot of the profile derivative with respect to the designated Kth model parameter; and 'diff2' gives the 2nd derivative of the profile with respect to the designated two parameters K and L. Additional arguments for the various cases:
		spectrum	none
		diff		<parameter K name> <dxK>
		diff2		<parameter K name> <dxK> <parameter L name> <dxL>

			Acceptable parameter names are:

		v0	centre velocity
		deltaV	full line width 
		S	total flux
		sigma	turbulent-broadening sigma
		f	fraction solid rotating
		B	asymmetry

	filterStyle	Possibilities are 'None', 'hanning_raw', 'hanning_sieve' or 'tukey_25'. What is usually meant by a 'Hanning filter' is 'hanning_sieve' - i.e. in which half the channels are discarded after applying the filter. 'hanning_raw' applies the Hanning filter but does not discard the channels. 'tukey_25' means a 25% Tukey filter such as was used for HIPASS.

	centreVel	The next 6 are the values of the 6 model parameters:
	lineWidth
	totalFlux
	turbBroadSigma
	fracSolidRot
	asymmetry

	chebyCoeffsStr	This should be a string of the form '<aa> <bb> ... <cc>'. The <aa>, <bb> etc are amplitudes in janskys of successive orders of Chebyshev polynomial which are used to provide a baseline. If you want a flat, zero-level baseline then supply an empty string ''.

	numChans	The number of spectral channels desired. This should be a power of 2 or at least a product of low primes to get best results from the Fast Fourier Transform used to construct the profile.

	refChan		This integer, together with the next argument 'refVel', is used to tie the velocity scale. If you want the line centred on channel N for example, supply N to this argument and the line centre velocity to 'refVel'.

		* NOTE 1: channels are counted from the left, starting from zero. Thus channel N is actually the N+1th channel in the spectrum.

		* NOTE 2: you should avoid placing a line too near the ends of the spectrum. You'll get artifacts if there is significant overlap with the spectrum ends. Bandpass pre-filtering avoids this in a real XF correlator, but this is not implemented in the present algorithm.

	refVel		See note to 'refChan' above.

	channelDelta	This specifies the velocity width of the (pre-filtered) spectrum channels. Use a negative value if you want the velocities to decrease from left to right.

		* NOTE 3: the constructed baseline function is added to the spectrum AFTER the order of the channels is decided. Hence changing the sign of 'channelDelta', while that will invert the order in which velocities are displayed, and also the profile itself, will have no effect on the baseline. In the examples given below for example the 1st-order Chebyshev component is negative. This leads to a baseline which slopes down from left to right regardless of whether 'channelDelta' is chosen negative or positive.

	The additional arguments (if any) have been specified already in the note to 'style'.

Examples:
---------

	./testbed.py spectrum None 521.0 173.0 0.049 8.0 0.2 0.1 '1.4e-4 -3.7e-5 8.2e-6' 256 99 765.6 -2.6

This generates a plot of a line with a central velocity of 521 km/s, a width of 173 km/s, and a total flux of 49 mJy km/s. Chebyshev components to order 2 (starting at zero) are added. No filtering is applied. 256 channels were desired with a channel spacing of -2.6 km/s.

	./testbed.py diff tukey_25 521.0 173.0 0.049 8.0 0.2 0.1 '1.4e-4 -3.7e-5 8.2e-6' 256 99 765.6 -2.6 deltaV 1.0

The plot here is a plot of the derivative of the line profile wrt the line-width parameter. The same profile specifications as previous are employed, except here a 25% Tukey filter is applied. An analytical expression for the derivative (red line) is compared to a finite-difference approximation of it (green dashes). The 'dxK' argument gives the deltaV differential to use in the finte-difference calculation.
"""

import numpy as nu
import pylab

from hispectrum.hiutils import local_exceptions as ex
from hispectrum.hiutils import misc_utils as mu
from hispectrum.hiutils import fitsWcs as wcs
from hispectrum.hiutils import priors
from hispectrum import hi_profile as hi

#.......................................................................
# Read command line arguments:
#
getNextCLArg = mu.GetNextCLArg()

style                   = getNextCLArg()	# spectrum, diff or diff2
filterStyle             = getNextCLArg()	# None, hanning_raw, hanning_sieve or tukey_25
centreVelKmPerSec       = getNextCLArg('float')	# eg. 521.0
lineWidthKmPerSec       = getNextCLArg('float')	# eg. 173.0
totalFluxJyKmPerSec     = getNextCLArg('float')	# eg. 0.049
turbBroadSigmaKmPerSec  = getNextCLArg('float')	# eg. 8.0
fracSolidRot            = getNextCLArg('float')	# eg. 0.2
asymmetryB              = getNextCLArg('float')	# eg. 0.1

chebyCoeffsStr          = getNextCLArg()	# eg. '0.14 -0.039'

numOutputChansRequested = getNextCLArg('int')	# eg. 256
refChanInOutput         = getNextCLArg('int')	# eg. 100
refVelKmPerSec          = getNextCLArg('float')	# eg. 765.6
channelDeltaKmPerSec    = getNextCLArg('float')	# eg. -5.2

firstChanOutput = 0
applyAsymmToSolid = True

if filterStyle=='None': filterStyle=None

chebyCoeffs = mu.strToList(chebyCoeffsStr, 'float')
numChebyOrders = len(chebyCoeffs)

parsSpecObj = hi.HIVanillaParsSpec(numChebyOrders=numChebyOrders)
velWCS = wcs.WCSAxisSimple('VELO', refChanInOutput+1.0, refVelKmPerSec, channelDeltaKmPerSec)
channelDesc = hi.ChannelDesc(velWCS, numOutputChansRequested)
profile = hi.HIProfileModel(parsSpecObj, channelDesc, filterStyle, applyAsymmToSolid)

velocitiesKmPerSec = refVelKmPerSec + channelDeltaKmPerSec * (nu.arange(profile.channelDesc.numChansOutput) - refChanInOutput)

namesList = ['v0','deltaV','S','sigma','f','A']

parValues = nu.zeros([profile.parsSpecObj.numPars], nu.float)
parValues[0] = centreVelKmPerSec
parValues[1] = lineWidthKmPerSec
parValues[2] = totalFluxJyKmPerSec
parValues[3] = turbBroadSigmaKmPerSec
parValues[4] = fracSolidRot
parValues[5] = asymmetryB
for oi in range(numChebyOrders):
  parValues[profile.parsSpecObj.numProfilePars+oi] = chebyCoeffs[oi]
  namesList.append('c%d' % oi)

if style=='spectrum':
  # Example call:
  #	./testbed.py spectrum None 521.0 173.0 0.049 8.0 0.2 0.1 '1.4e-4 -3.7e-5 8.2e-6' 256 99 765.6 -2.6
  fluxDensities_mJy = profile.calcModelValues(parValues)*1000.0

  pylab.plot(velocitiesKmPerSec, fluxDensities_mJy, 'b-')
  minX = min(velocitiesKmPerSec)
  maxX = max(velocitiesKmPerSec)
  minY = min(fluxDensities_mJy)
  maxY = max(fluxDensities_mJy)
  (worldXLo, worldXHi, worldYLo, worldYHi) = mu.doPadLimits(velocitiesKmPerSec[0]\
    , velocitiesKmPerSec[-1], fluxDensities_mJy.min(), fluxDensities_mJy.max())
  pylab.axis([worldXLo, worldXHi, worldYLo, worldYHi])
  pylab.xlabel('Recession velocity (km/s)')
  pylab.ylabel('Flux density (mJy)')
  pylab.title('Simulated HI profile')
  pylab.show()


elif style=='diff':
  # Example calls:
  #	./testbed.py diff None 521.0 173.0 0.049 8.0 0.2 0.1 '1.4e-4 -3.7e-5 8.2e-6' 256 99 765.6 -2.6 v0 1.0
  #
  #	./testbed.py diff None 521.0 173.0 0.049 8.0 0.2 0.1 '' 256 99 765.6 -2.6 v0 1.0
  #	./testbed.py diff None 521.0 173.0 0.049 8.0 0.2 0.1 '' 256 99 765.6 -2.6 deltaV 1.0
  #	./testbed.py diff None 521.0 173.0 0.049 8.0 0.2 0.1 '' 256 99 765.6 -2.6 S 0.001
  #	./testbed.py diff None 521.0 173.0 0.049 8.0 0.2 0.1 '' 256 99 765.6 -2.6 sigma 0.1
  #	./testbed.py diff None 521.0 173.0 0.049 8.0 0.2 0.1 '' 256 99 765.6 -2.6 f 0.01
  #	./testbed.py diff None 521.0 173.0 0.049 8.0 0.2 0.1 '' 256 99 765.6 -2.6 A 0.02

  varStr = getNextCLArg()	# recognized values: v0, deltaV, S, sigma, f, A.
  dx     = getNextCLArg('float')

  k = namesList.index(varStr)
  diffValsTheory = profile.calcDMByDParK(parValues, k)
  diffValuesNumeric = profile.estFirstDerivByFD(parValues, k, dx)

  pylab.plot(velocitiesKmPerSec, diffValuesNumeric, 'r-')
  pylab.plot(velocitiesKmPerSec, diffValsTheory, 'g--')
  pylab.show()

elif style=='diff2':
  # Example calls:
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 v0 1.0 v0 1.0
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 v0 1.0 deltaV 1.0
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 v0 1.0 S 0.001
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 v0 1.0 sigma 0.1
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 v0 1.0 f 0.01
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 v0 1.0 A 0.02

  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 deltaV 1.0 deltaV 1.0
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 deltaV 1.0 S 0.001
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 deltaV 1.0 sigma 0.1
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 deltaV 1.0 f 0.01
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 deltaV 1.0 A 0.02

  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 S 0.001 S 0.001 (this one is zero for all velocities)
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 S 0.001 sigma 0.1
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 S 0.001 f 0.01
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 S 0.001 A 0.02

  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 sigma 0.1 sigma 0.1
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 sigma 0.1 f 0.01
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 sigma 0.1 A 0.02

  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 f 0.01 f 0.01 (this one is zero for all velocities)
  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 f 0.01 A 0.02

  #	./testbed.py diff2 None 521.0 173.0 0.049 8.0 0.9 0.5 '' 256 99 765.6 -2.6 A 0.02 A 0.02 (this one is zero for all velocities)

  varKStr = getNextCLArg()	# recognized values: v0, deltaV, S, sigma, f, A.
  dxK     = getNextCLArg('float')
  varLStr = getNextCLArg()	# recognized values: v0, deltaV, S, sigma, f, A.
  dxL     = getNextCLArg('float')

  k = namesList.index(varKStr)
  l = namesList.index(varLStr)
  if l<k: (l,k) = (k,l)
  diffValsTheory = profile.calcD2MByDParKParL(parValues, k, l)
  diffValuesNumeric = profile.estSecondDerivByFD(parValues, k, l, dxK, dxL)

  pylab.plot(velocitiesKmPerSec, diffValuesNumeric, 'r-')
  pylab.plot(velocitiesKmPerSec, diffValsTheory, 'g--')
  pylab.show()

else:
  raise ex.UnrecognizedChoiceObject(style)





