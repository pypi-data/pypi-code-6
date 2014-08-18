import numpy as np
import bob
import os
import pdb # Debugging

from spear.tools import IVecTool 

from fastPLDA import *
from . import TwoCovPLDA
from . import TwoStagePLDA

class fastPLDA (IVecTool):

    ########### PLDA training ############
    def train_plda_enroler(self, all_train_files, plda_enroler_file):
        # load GMM stats from training files
        all_training_features = []
        for train_files in all_train_files:
            training_features = self.load_ivectors_by_client(train_files)
            all_training_features.append(training_features)
        input_dimension = all_training_features[0][0].shape[1]
    
        print("  -> Training PLDA base machine")
        if self.m_config.PLDA_TYPE == 'scalable':
            # create trainer
            t = bob.trainer.PLDATrainer(self.m_config.PLDA_TRAINING_ITERATIONS)
            t.seed = self.m_config.INIT_SEED
            t.init_f_method = self.m_config.INIT_F_METHOD
            t.init_f_ratio = self.m_config.INIT_F_RATIO
            t.init_g_method = self.m_config.INIT_G_METHOD
            t.init_g_ratio = self.m_config.INIT_G_RATIO
            t.init_sigma_method = self.m_config.INIT_S_METHOD
            t.init_sigma_ratio = self.m_config.INIT_S_RATIO
            # train machine
            self.m_plda_base = bob.machine.PLDABase(input_dimension, self.m_config.SUBSPACE_DIMENSION_OF_F, self.m_config.SUBSPACE_DIMENSION_OF_G, self.m_config.variance_flooring)
            t.train(self.m_plda_base, all_training_features[0])
            # write machines to file
            proj_hdf5file = bob.io.HDF5File(str(plda_enroler_file), "w")
            self.m_plda_base.save(proj_hdf5file) 
        
        elif self.m_config.PLDA_TYPE == 'scalable&fast':
            # Check how many filelists were provided. If there are two of them -
            # run two-stage PLDA
            if len(all_train_files) == 2:
                ## TWO-STAGE PLDA
                # create trainer
                t = TwoStagePLDA.TwoStagePLDATrainer((self.m_config.PLDA_TRAINING_ITERATIONS, 
                    self.m_config.TWO_STAGE_PLDA_TRAINING_ITERATIONS), self.m_config)
                # train machine
                self.m_plda_base = fastPLDABase(input_dimension, self.m_config.SUBSPACE_DIMENSION_OF_V, self.m_config.SUBSPACE_DIMENSION_OF_U)
                t.train(self.m_plda_base, all_training_features[0], all_training_features[1])
                # write machines to file
                self.m_plda_base.save(plda_enroler_file)
                # initialize the conveyor for plda scoring
                self.plda_conveyor = fastPLDAConveyor(self.m_plda_base)
            elif len(all_train_files) == 1:
      
                if self.m_config.FAST_PLDA_TYPE == 'two-cov':
                    # create trainer
                    t = TwoCovPLDA.twoCovTrainer(self.m_config.PLDA_TRAINING_ITERATIONS, 
                                                 self.m_config)
                    # train machine
                    self.m_plda_base = TwoCovPLDA.twoCovBase(input_dimension)
                    t.train(self.m_plda_base, all_training_features[0])
                    # write machines to file
                    self.m_plda_base.save(plda_enroler_file)
                    # initialize the conveyor for plda scoring
                    self.plda_conveyor = TwoCovPLDA.twoCovConveyor(self.m_plda_base)          
                else:
                    # create trainer
                    t = fastPLDATrainer(self.m_config.PLDA_TRAINING_ITERATIONS, self.m_config)
                    # train machine
                    self.m_plda_base = fastPLDABase(input_dimension, self.m_config.SUBSPACE_DIMENSION_OF_V, self.m_config.SUBSPACE_DIMENSION_OF_U)
                    t.train(self.m_plda_base, all_training_features[0])
                    # write machines to file
                    self.m_plda_base.save(plda_enroler_file)
                    # initialize the conveyor for plda scoring
                    self.plda_conveyor = fastPLDAConveyor(self.m_plda_base)
            else:
                raise RuntimeError('Too many filelists')
        else:
          raise RuntimeError('Unknown PLDA type')
   
    def load_plda_enroler(self, plda_enroler_file):
        """Reads the PLDA model from file"""
        if self.m_config.PLDA_TYPE == 'scalable':
            proj_hdf5file = bob.io.HDF5File(plda_enroler_file)
            self.m_plda_base = bob.machine.PLDABase(proj_hdf5file)
            self.m_plda_machine = bob.machine.PLDAMachine(self.m_plda_base)
            self.m_plda_trainer = bob.trainer.PLDATrainer()
    
        elif self.m_config.PLDA_TYPE == 'scalable&fast':
            f = bob.io.HDF5File(plda_enroler_file)
            if self.m_config.FAST_PLDA_TYPE == 'two-cov':
                dim_d = f.read('dim_d') 
                self.m_plda_base = TwoCovPLDA.twoCovBase(dim_d) 
                self.m_plda_base.invB = f.read('invB')
                self.m_plda_base.invW = f.read('invW')
                self.m_plda_base.mu = f.read('mu')
                self.plda_conveyor = TwoCovPLDA.twoCovConveyor(self.m_plda_base)
            else:
                dim_d = f.read('dim_d')
                dim_V = f.read('dim_V')
                dim_U = f.read('dim_U')
                self.m_plda_base = fastPLDABase(dim_d, dim_V, dim_U)
                self.m_plda_base.V = f.read('V')

                if dim_U > 0:
                    self.m_plda_base.U = f.read('U')
                else:
                    self.m_plda_base.U = np.zeros((dim_d,0))
              
                self.m_plda_base.mu = f.read('mu')
                self.m_plda_base.Sigma = f.read('Sigma')
                self.m_plda_base.dim_d = dim_d
                self.m_plda_base.dim_V = dim_V
                self.m_plda_base.dim_U = dim_U
                self.plda_conveyor = fastPLDAConveyor(self.m_plda_base)
