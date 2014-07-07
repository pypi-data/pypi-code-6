#!/usr/bin/env python

# Author: Ian Stewart
#
# Contents:
#	generateChebyshevSamples
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
# * Copied to this release version.
# * Replaces a 'for' by a numpy vector operation to increase speed.
#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_module_name = 'chebyshev'

import numpy as nu

#import misc_utils as mu

def generateChebyshevSamples(numSamples, numOrders):
  """Generates a block of samples of Chebyshev polynomials of the first kind."""

  chebyshevs = nu.ones([numSamples, numOrders], nu.float)
  if numOrders>1:
#    for i in range(numSamples):
#      chebyshevs[i,1] = mu.fracVal(-1.0, 1.0, (i+0.5)/float(numSamples))
    chebyshevs[:,1] = ((nu.arange(numSamples)+0.5)/float(numSamples))*2.0 - 1.0
    for oi in range(2,numOrders):
      chebyshevs[:,oi] = 2.0*chebyshevs[:,1]*chebyshevs[:,oi-1] - chebyshevs[:,oi-2]

  return chebyshevs

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  pass

