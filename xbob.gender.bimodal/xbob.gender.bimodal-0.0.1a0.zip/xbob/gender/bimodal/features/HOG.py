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

class HOG (facereclib.features.Extractor):
  """Extractor HOG"""

  def __init__(
      self,
      height,
      width,
      nb_bins = 8,
      full_orientation = False,
      # Cell setup
      cell_size = 4,    # one or two parameters for cell size
      cell_overlap = 0, # one or two parameters for cell overlap
      # Block setup
      block_size = 4,    # one or two parameters for block size
      block_overlap = 0, # one or two parameters for block overlap
  ):
    """Initializes the local Gabor binary pattern histogram sequence tool chain with the given file selector object"""

    # call base class constructor
    facereclib.features.Extractor.__init__(
        self,
        height = height,
        width = width,
        full_orientation = full_orientation,
        cell_size = cell_size,
        cell_overlap = cell_overlap,
        block_size = block_size,
        block_overlap = block_overlap,
    )

    # cell parameters
    self.m_cell_size = cell_size if isinstance(cell_size, (tuple, list)) else (cell_size, cell_size)
    self.m_cell_overlap = cell_overlap if isinstance(cell_overlap, (tuple, list)) else (cell_overlap, cell_overlap)
    if self.m_cell_size[0] < self.m_cell_overlap[0] or self.m_cell_size[1] < self.m_cell_overlap[1]:
      raise ValueError("The overlap is bigger than the cell size. This won't work. Please check your setup!")
    # block parameters
    self.m_block_size = block_size if isinstance(block_size, (tuple, list)) else (block_size, block_size)
    self.m_block_overlap = block_overlap if isinstance(block_overlap, (tuple, list)) else (block_overlap, block_overlap)
    if self.m_block_size[0] < self.m_block_overlap[0] or self.m_block_size[1] < self.m_block_overlap[1]:
      raise ValueError("The overlap is bigger than the block size. This won't work. Please check your setup!")

    self.m_hog_extractor = bob.ip.HOG(
          height = height,
          width = width,
          nb_bins = nb_bins,
          full_orientation = full_orientation,
          cell_y = self.m_cell_size[0],
          cell_x = self.m_cell_size[1],
          cell_ov_y = self.m_cell_overlap[0],
          cell_ov_x = self.m_cell_overlap[1],
          block_y = self.m_block_size[0],
          block_x = self.m_block_size[1],
          block_ov_y = self.m_block_overlap[0],
          block_ov_x = self.m_block_overlap[1]
    )


  def __call__(self, image):
    """Extracts HOGs from the given image"""
    # Computes HOG histograms
    return self.m_hog_extractor(image)

