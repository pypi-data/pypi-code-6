"""This file implements functionality for the two-stage PLDA model"""

import numpy as np

from fastPLDA import *

class TwoStagePLDATrainer(fastPLDATrainer):
    """Train the PLDA model with an additional subspace for a second stage.
    
    Attributes:
        training_iterations: Maximum number of the training iterations for the
                             first stage.
        training_iterations2: Maximum number of the training iterations for the
                              second stage.
        seed: Seed for the random number generator.
        init_V_method: A method to initialize V matrix.
        init_U_method: A method to initialize U matrix for the first stage.
        init_U2_method: A method to initialize U matrix for the second stage.
        init_Sigma_method: A method to initialize Sigma matrix.
        training_threshold: Threshold for ending the EM loop.
        do_md_step: Indicator for the minimum-divergence step.
        compute_log_likelihood: Indication whether to compute a log-likelihood
                                of the training data during EM-algorithm
        Sigma_scale: Parameter that multiplies initial Sigma matrix
    """
    def __init__(self, training_iterations, config=None):
        """
        Args:
            training_iterations: A tuple, containing the maximum number of the 
                                 training iterations for both stages.
            config: A class with the following fields: 
                INIT_SEED: A seed for the random number generator.
                INIT_V_METHOD: A method to initialize V matrix.
                INIT_U_METHOD: A method to initialize U matrix for the first 
                                stage.
                INIT_U2_METHOD: A method to initialize U matrix for the second 
                                stage.
                INIT_SIGMA_METHOD: A method to initialize Sigma matrix.
                PLDA_TRAINING_THRESHOLD: A threshold for ending the EM loop.
                PLDA_DO_MD_STEP: An indicator for the minimum-divergence step.
                PLDA_COMPUTE_LOG_LIKELIHOOD: An indicator for the log-likelihood
                                             computation.
                INIT_SIGMA_SCALE: A parameter that multiplies initial Sigma 
                                  matrix.
                SUBSPACE_DIMENSION_OF_U2: A number of dimension of U matrix for
                                          the second stage of learning.
        """
        self.training_iterations2 = training_iterations[1]
        fastPLDATrainer.__init__(self, training_iterations[0], config)
        
        if config is not None:
            self.init_U2_method = config.INIT_U2_METHOD
            self.dim_U2 = config.SUBSPACE_DIMENSION_OF_U2
            
    def train(self, pldabase, data1, data2):
        """Train the parameters for the two-stage PLDA model.
        
        Args:
            pldabase: An instance of newPLDABase class to store the parameters.
            data1: A list of ndarrays for the first stage. Each person has its 
                   own list item of the shape 
                   (number_of_samples, number_of_features)
            data2: A list of ndarrays for the first stage. Each person has its 
                   own list item of the shape 
                   (number_of_samples, number_of_features)
        """
        ## FIRST STAGE
        print 'Training of the first stage with %d identities' % len(data1)
        fastPLDATrainer.train(self, pldabase, data1)
        
        ## SECOND STAGE
        print 'Training of the second stage with %d identities' % len(data2)
        data, pooled_data, N, f, S = self._preprocessing(pldabase, data2)
        
        # Initialize PLDA parameters
        self.__initialize(pldabase) 
        
        for i in xrange(self.training_iterations2):
            junk, T_x, R_yy, R_yx, R_xx, junk = self._e_step(pldabase, data, N, 
                                                            f, S)
            self.__m_step(pldabase, R_yx, R_xx, T_x)
            if self.do_md_step:
                self.__md_step(pldabase, R_yy, R_yx, R_xx, N) 
            
            # Print current progress
            self._print_progress(pldabase, pooled_data, i)
    
    def __initialize(self, pldabase):
        """Initialize the parameters for the second stage of the two-stage
        PLDA model.
        
        Args:
            pldabase: An instance of the newPLDABase class.
        """
        # Integrate out channel latent variable and set the model to be
        # simplified one.
        pldabase.Sigma += np.dot(pldabase.U, pldabase.U.T)
        self.plda_type = 'simp'
        
        pldabase.dim_U = self.dim_U2
        if self.init_U2_method == 'random':
            pldabase.U = np.random.randn(pldabase.dim_d, pldabase.dim_U)
        else:
            raise RuntimeError('Unknown init_U2_method')
    
    @staticmethod    
    def __m_step(pldabase, R_yx, R_xx, T_x):
        """Performs M-step for the second stage of the two-stage PLDA learning.
        
        Args:
            pldabase: An instance of newPLDABase class.
            R_yx: A posterior covariance matrix between 'y' and 'x' variables of 
                  the shape (dim_V, dim_U).
            R_xx: A posterior covariance matrix between 'x' variables of the 
                  shape (dim_U, dim_U).
            T_x: A matrix with the summed multiplication between the posterior 
                 expectations of the latent channel variables and the 
                 corresponding data samples. It has the following shape: 
                 (dim_U, dim_d).
        """
        pldabase.U = np.linalg.solve(R_xx, T_x - np.dot(pldabase.V, R_yx).T).T
    
    @staticmethod
    def __md_step(pldabase, R_yy, R_yx, R_xx, N):
        """Performs minimum-divergence step for the two-stage PLDA learning.
        
        Args:
            pldabase: An instance of newPLDABase class.
            R_yy: A posterior covariance matrix between 'y' variables of the 
                  shape (dim_V, dim_V).
            R_yx: A posterior covariance matrix between 'y' and 'x' variables of 
                  the shape (dim_V, dim_U).
            R_xx: A posterior covariance matrix between 'x' variables of the 
                  shape (dim_U, dim_U).
            N: Total number of files.
        """
        G = np.linalg.solve(R_yy.T, R_yx).T  # G = R_yx' / R_yy;
        X_md = (R_xx - np.dot(G, R_yx)) / N
        pldabase.U = np.dot(pldabase.U, np.linalg.cholesky(X_md))
        pldabase.V += np.dot(pldabase.U, G)

