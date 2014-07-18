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

from facereclib.tools import UBMGMM as FaceUBMGMM
from facereclib import utils

class UBMGMM (FaceUBMGMM):
  """Tool for computing Universal Background Models and Gaussian Mixture Models of the features"""

  def __init__(
      self,
      **kwargs
  ):
    """Initializes the local UBM-GMM tool chain with the given file selector object"""

    # call base class constructor and register that this tool performs projection
    FaceUBMGMM.__init__(
        self,
        **kwargs
    )

  #######################################################
  ################ UBM training #########################

  def _train_projector_using_array(self, array):

    utils.debug(" .... Training with %d feature vectors" % array.shape[0])

    # Computes input size
    input_size = array.shape[1]

    # Normalizes the array if required
    utils.debug(" .... Normalizing the array")
    if not self.m_normalize_before_k_means:
      normalized_array = array
    else:
      normalized_array, std_array = self.__normalize_std_array__(array)


    # Creates the machines (KMeans and GMM)
    utils.debug(" .... Creating machines")
    kmeans = bob.machine.KMeansMachine(self.m_gaussians, input_size)
    self.m_ubm = bob.machine.GMMMachine(self.m_gaussians, input_size)

    # Creates the KMeansTrainer
    kmeans_trainer = bob.trainer.KMeansTrainer()
    kmeans_trainer.rng = bob.core.random.mt19937(self.m_init_seed)
    kmeans_trainer.convergence_threshold = self.m_training_threshold
    kmeans_trainer.max_iterations = self.m_k_means_training_iterations

    # Trains using the KMeansTrainer
    utils.info("  -> Training K-Means")
    kmeans_trainer.train(kmeans, normalized_array)

    [variances, weights] = kmeans.get_variances_and_weights_for_each_cluster(normalized_array)
    means = kmeans.means

    # Undoes the normalization
    utils.debug(" .... Undoing normalization")
    if self.m_normalize_before_k_means:
      self.__multiply_vectors_by_factors__(means, std_array)
      self.__multiply_vectors_by_factors__(variances, std_array ** 2)

    # Initializes the GMM
    self.m_ubm.means = means
    self.m_ubm.variances = variances
    self.m_ubm.weights = weights
    self.m_ubm.set_variance_thresholds(self.m_variance_threshold)

    # Trains the GMM
    utils.info("  -> Training GMM")
    trainer = bob.trainer.ML_GMMTrainer(self.m_update_means, self.m_update_variances, self.m_update_weights)
    trainer.rng = bob.core.random.mt19937(self.m_init_seed)
    trainer.convergence_threshold = self.m_training_threshold
    trainer.max_iterations = self.m_gmm_training_iterations
    trainer.train(self.m_ubm, array)

