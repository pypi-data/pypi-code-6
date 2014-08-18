#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <Pedro.Tome@idiap.ch>

# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy.random
import scipy.ndimage
import scipy.signal
import bob


def imfilter(a, b, gpu=False, conv=True):
  """imfilter function based on MATLAB implementation."""
  if (a.dtype == numpy.uint8):
      a= bob.core.convert(a,numpy.float64,(0,1))    
  M, N = a.shape
  if conv == True:
      b = bob.ip.rotate(b, 180)    
  shape = numpy.array((0,0))
  shape[0] = a.shape[0] + b.shape[0] - 1
  shape[1] = a.shape[1] + b.shape[1] - 1
  a_ext = numpy.ndarray(shape=shape, dtype=numpy.float64)
  bob.sp.extrapolate_nearest(a, a_ext)
  
  if gpu == True:
    import xbob.cusp
    return xbob.cusp.conv(a_ext, b)
  else:
    return scipy.signal.convolve2d(a_ext, b, 'valid')



