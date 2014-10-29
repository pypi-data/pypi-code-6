"""
top-level script to perform feature selection using two kernels
"""

# common modules
import scipy as sp
import numpy as np
import pylab
import pandas as pd

# sklearn
from sklearn.linear_model import RidgeCV, Ridge
from sklearn.cross_validation import KFold, LeaveOneOut, ShuffleSplit
from sklearn.metrics import mean_squared_error

# project
from fastlmm.pyplink.snpreader.Bed import Bed, SnpAndSetName, PositionRange
import fastlmm.pyplink.plink as plink
import logging


def select_num_pcs(pcs, pheno, num_steps):
    """
    run cross-validation to determine best number of pcs
    """

    max_num = pcs.shape[1]
    num_samples = pcs.shape[0]

    assert len(pheno) == num_samples

    num_pcs_grid = np.logspace(0, max_num, endpoint=True, num=num_steps, base=2.0)
    
    num_folds = 5
    kfold = KFold(num_samples, num_folds)

    performance = np.zeros((num_pcs, num_folds))

    for pc_idx, num_pcs in enumerate(num_pcs_grid):
        for k_idx, (train_idx, test_idx) in enumerate(kfold):
            X_train = pcs[train_idx][0:num_pcs]
            y_train = pheno[train_idx]
            
            # determine regularization parameter using built-in LOOCV
            ridge_cv = RidgeCV()
            ridge_cv.fit(X_train, y_train)

            X_test = pcs[test_idx][0:num_pcs]
            y_test = pheno[test_idx]

            y_pred = ridge_cv.predict(X_test)

            performance[k_idx, pc_idx] = mean_squared_error(y_test, y_pred)

    import ipdb
    ipdb.set_trace()
    mean_perf = performance.mean(axis=0)


def fancy_xval(snps):
    """
    first draft of implementation discussed with christoph
    """

    U, s, V = np.linalg.svd(snps, full_matrices=True)

    K_inv = (U * 1/s)


def test():

    
    # set up data
    ##############################
    
    bed_fn = "examples/toydata"
    pheno_fn = "examples/toydata.phe"

    # get PCs
    from fastlmm.util.computePC import computePC
    eig_val, pcs = computePC(file=bed_fn)

    # load pheno
    i_pheno = 0
    pheno = plink.loadOnePhen(pheno_fn, i_pheno)
    ind_iid = pheno['iid']
    y = pheno['vals'][:,0]

    # set up grid
    ##############################
    num_steps = 5

    select_num_pcs(pcs, y, num_steps)


if __name__ == "__main__":
    test()

