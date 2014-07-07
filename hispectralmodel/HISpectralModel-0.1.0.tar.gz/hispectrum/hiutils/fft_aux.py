#!/usr/bin/env python
#
# Name:                         fft_aux
#
# Author: Ian Stewart
#
# Contains:
#	doHermitianCopy
#	findNextHighest2357multiple
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
# - Deleted calcFftwRedundantXSize, convolveImage and the test harness.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_module_name = 'fft_aux'

"""This module ports some utility functions from ssclib/src/fftw3_aux.f90."""

import math
import numpy as nu

#import SciMathConstants as const
#import misc_utils as mu

#.......................................................................
class IllegalCentralValue(Exception):
  def __init__(self, numElements, foldPixel, centralValue):
    self.numElements = numElements
    self.foldPixel = foldPixel
    self.centralValue = centralValue
  def __str__(self):
    return "The input vector has an even number of elements %d - that means the %dth element must be real-valued to permit a Hermitian result. But it isn't, it is %s." % (self.numElements, self.foldPixel, self.centralValue)

#.......................................................................
def doHermitianCopy(inVector, nullifyCentralImaginary=False):
  """The argument inVector is taken to be a 1-dimensional numpy array of complex values. The task of the function is to reflect-copy the conjugates of the values in the bottom half of the vector into the top half. That way the result will be Hermitian and thus have a real-valued Fourier transform.

The problems lie in the definition of the word 'half'. This varies slightly depending on whether there is an odd or an even number of elements in the vector. The difference is illustrated by two examples, the first of which has an odd number, the second an even number.

Odd example: N = 9. Values from 0 to N//2 must be filled.

	Element:	 0    1    2    3    4    5    6    7    8
	Value before:	9+2j 8-4j 6+0j 2+2j 1-3j 0+0j 0+0j 0+0j 0+0j
	Value after:	9+2j 8-4j 6+0j 2+2j 1-3j 1+3j 2-2j 6+0j 8+4j

Even example: N = 8. Values from 0 to N//2 must be filled; however inVector[N//2] must be real for the output to be Hermitian. The function will stop with an error if this is not true.

	Element:	 0    1    2    3    4    5    6    7
	Value before:	9+2j 8-4j 6+0j 2+2j 1+0j 0+0j 0+0j 0+0j
	Value after:	9+2j 8-4j 6+0j 2+2j 1+0j 2-2j 6+0j 8+4j

Note that in no case is the inVector[0] value copied. This is because this corresponds to frequency zero, hence is its own negative frequency.
  """

########## should check (or enforce) that inVector[0].imag==0!

  numElements = inVector.shape[0]
  foldPixel = (numElements+1) // 2

  if numElements%2==0: # numElements is even. Check the central value is real.
    if not inVector[foldPixel].imag==0.0:
      if nullifyCentralImaginary:
        inVector[foldPixel] = complex(inVector[foldPixel].real, 0.0)
      else: 
        raise IllegalCentralValue(numElements, foldPixel, inVector[foldPixel])

  inVector[numElements:numElements-foldPixel:-1] = inVector[1:foldPixel].conjugate()
  return inVector

#.......................................................................
def findNextHighest2357multiple(i):
    """The original f90 header comment ran as follows:

  ! This is designed to look for the smallest integer that satisfies the
  ! following conditions: (i) it is greater than or equal to the argument
  ! i; (ii) it is a product only of the numbers 2, 3, 5 and 7. The library
  ! fftw works most efficiently on arrays that have the second property,
  ! so images are padded in size (i) to prevent any 'wrapping' of the
  ! convolver and (ii) so they have dimensions divisable by 2, 3, 5 and/or 7.
    """

    lnTwo   = math.log(2.0)
    lnThree = math.log(3.0)
    lnFive  = math.log(5.0)
    lnSeven = math.log(7.0)

    lni = math.log(float(i))

#    maxai = 1 + int(lni / const.lnTwo)
#    maxbi = 1 + int(lni / const.lnThree)
#    maxci = 1 + int(lni / const.lnFive)
#    maxdi = 1 + int(lni / const.lnSeven)
    maxai = 1 + int(lni / lnTwo)
    maxbi = 1 + int(lni / lnThree)
    maxci = 1 + int(lni / lnFive)
    maxdi = 1 + int(lni / lnSeven)

    firstOver = True
    bestTerm = 0.0 # just to define it, so the inner 'if' generates no
    # complaints from the compiler.
    for ai in range(maxai+1):
      for bi in range(maxbi+1):
        for ci in range(maxci+1):
          for di in range(maxdi+1):
#            term = ai * const.lnTwo + bi * const.lnThree + ci * const.lnFive + di * const.lnSeven
            term = ai * lnTwo + bi * lnThree + ci * lnFive + di * lnSeven
            if (term >= lni and (term < bestTerm or firstOver)):
              bestTerm = term
              besta = ai
              bestb = bi
              bestc = ci
              bestd = di

              if (firstOver): firstOver = False

              break

    result = (2**besta) * (3**bestb) * (5**bestc) * (7**bestd)
    return result


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  pass

