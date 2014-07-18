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

from facereclib.tools.ISV import ISV as FaceISV
from facereclib import utils
import bob
import os

class ISV (FaceISV):
  """Tool chain for computing Unified Background Models and Gaussian Mixture Models of the features"""

  
  def __init__(self, **kwargs):
    """Initializes the local UBM-GMM tool with the given file selector object"""
    # call base class constructor
    FaceISV.__init__(self, **kwargs)

  def __load_gmm_stats_list__(self, ld_files):
    """Loads a list of lists of GMM statistics from a list of dictionaries of filenames
       There is one list for each identity"""
    # Initializes a python list for the GMMStats
    gmm_stats = [] 
    for k in sorted(ld_files.keys(), key=lambda x: x.id): 
      # Loads the list of GMMStats for the given client
      gmm_stats_c = self.__load_gmm_stats__(ld_files[k])
      # Appends to the main list 
      gmm_stats.append(gmm_stats_c)
    return gmm_stats

  def _train_isv(self, data):
    """Train the ISV model given a dataset"""
    utils.info("  -> Training ISV enroller")
    self.m_isvbase = bob.machine.ISVBase(self.m_ubm, self.m_subspace_dimension_of_u)
    # train ISV model
    self.m_isvtrainer = bob.trainer.ISVTrainer(self.m_isv_training_iterations, self.m_relevance_factor)
    self.m_isvtrainer.rng = bob.core.random.mt19937(self.m_init_seed)
    self.m_isvtrainer.train(self.m_isvbase, data)

  def _save_projector_isv_resolved(self, isv_filename):
    self.m_isvbase.save(bob.io.HDF5File(isv_filename, "w"))
    base_dir = os.path.dirname(isv_filename)
    bob.io.save(self.m_isvtrainer.__Z__[0], os.path.join(base_dir, 'zf.hdf5'))
    bob.io.save(self.m_isvtrainer.__Z__[1], os.path.join(base_dir, 'zm.hdf5'))
