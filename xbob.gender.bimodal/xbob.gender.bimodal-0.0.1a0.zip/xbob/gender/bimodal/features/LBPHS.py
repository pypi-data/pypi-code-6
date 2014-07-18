#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
#
# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bob
import numpy
import math
import facereclib

class LBPHS (facereclib.features.Extractor):
  """Extractor for local binary pattern histogram sequences"""

  def __init__(
      self,
      # Block setup
      block_size,    # one or two parameters for block size
      block_overlap = 0, # one or two parameters for block overlap
      # LBP parameters
      lbp_radius = 2,
      lbp_neighbor_count = 8,
      lbp_uniform = True,
      lbp_circular = True,
      lbp_rotation_invariant = False,
      lbp_compare_to_average = False,
      lbp_add_average = False,
  ):
    """Initializes the local Gabor binary pattern histogram sequence tool chain with the given file selector object"""

    # call base class constructor
    facereclib.features.Extractor.__init__(
        self,

        block_size = block_size,
        block_overlap = block_overlap,
        lbp_radius = lbp_radius,
        lbp_neighbor_count = lbp_neighbor_count,
        lbp_uniform = lbp_uniform,
        lbp_circular = lbp_circular,
        lbp_rotation_invariant = lbp_rotation_invariant,
        lbp_compare_to_average = lbp_compare_to_average,
        lbp_add_average = lbp_add_average,
    )

    # block parameters
    self.m_block_size = block_size if isinstance(block_size, (tuple, list)) else (block_size, block_size)
    self.m_block_overlap = block_overlap if isinstance(block_overlap, (tuple, list)) else (block_overlap, block_overlap)
    if self.m_block_size[0] < self.m_block_overlap[0] or self.m_block_size[1] < self.m_block_overlap[1]:
      raise ValueError("The overlap is bigger than the block size. This won't work. Please check your setup!")

    # Initializes LBPHS processor
    real_h = self.m_block_size[0] + 2 * lbp_radius
    real_w = self.m_block_size[1] + 2 * lbp_radius
    real_oy = self.m_block_overlap[0] + 2 * lbp_radius
    real_ox = self.m_block_overlap[1] + 2 * lbp_radius

    self.m_lbphs_extractor = bob.ip.LBPHSFeatures(
          block_h = real_h,
          block_w = real_w,
          overlap_h = real_oy,
          overlap_w = real_ox,
          lbp_radius = float(lbp_radius),
          lbp_neighbours = lbp_neighbor_count,
          circular = lbp_circular,
          to_average = lbp_compare_to_average,
          add_average_bit = lbp_add_average,
          uniform = lbp_uniform,
          rotation_invariant = lbp_rotation_invariant
    )

  def __call__(self, image):
    """Extracts the local binary pattern histogram sequence from the given image"""
    # Computes LBP histograms
    abs_blocks = self.m_lbphs_extractor(image)

    # Converts to Blitz array (of different dimensionalities)
    self.m_n_bins = self.m_lbphs_extractor.n_bins
    self.m_n_blocks = len(abs_blocks)

    return numpy.hstack(abs_blocks).astype(numpy.float64)

