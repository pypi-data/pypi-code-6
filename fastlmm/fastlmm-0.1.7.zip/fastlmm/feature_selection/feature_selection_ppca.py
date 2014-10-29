"""
select number of PCs efficiently
"""


import numpy as np
import scipy as sp

from sklearn.metrics import mean_squared_error
from fastlmm.pyplink.snpreader.Bed import Bed
import fastlmm.pyplink.plink as plink
from fastlmm.feature_selection.PerformSelectionDistributable import build_kernel_blocked
import fastlmm.util.standardizer as stdizer
from sklearn.cross_validation import KFold
import logging
import fastlmm.util.util as util 
import fastlmm.inference as fastlmm
from fastlmm.util.pickle_io import save, load

import cPickle
import bz2
import sys


def run_ppca():
    logging.basicConfig(level=logging.INFO)

    standardizer = stdizer.Unit()

    # set up data
    ##############################
    #
    bed_reader = Bed("G:\Genetics/dbgap/ARIC/autosomes.genic")
    #bed_reader = Bed("examples/toydata")
    pheno_fn = "examples/toydata.phe"
    
    geno = bed_reader.read(order='C')
    G = geno['snps']
    G = standardizer.standardize(G)
    
    print "dimensionality:", G.shape

    print "starting pca"

    import sklearn
    ppca = sklearn.decomposition.ProbabilisticPCA(n_components='mle')
    ppca.fit(G.T)

    print "pca done"

    n_components_pca_mle = ppca.n_components

    print "number of components selected:", n_components_pca_mle
 



def factor(S, U, y):
    ###############################

    y -= y.mean()

    num_ind = len(y)



    n_folds = 8
    n_pc_grid = 6
    n_deltas = 4

    grid_pcs = np.logspace(0, np.log2(1000), base=2.0, num=n_pc_grid, endpoint=True)
    grid_delta = np.logspace(-2, 6, base=np.exp(1), num=n_deltas, endpoint=True)

    perf = np.zeros((n_folds, n_deltas, n_pc_grid))
    ll = np.zeros((n_folds, n_deltas, n_pc_grid))

    for kfold_idx, (train_idx, test_idx) in enumerate(KFold(num_ind, n_folds=n_folds)):

        print "running fold", kfold_idx

        y_train = y[train_idx]
        y_test = y[test_idx]
        U_train = U[train_idx]
        U_test = U[test_idx]

        U_train_y = U_train.T.dot(y_train)
        n_test = len(test_idx)

        
        for pc_idx, num_pcs in enumerate(grid_pcs):

            num_pcs = int(num_pcs)

            print "num_pcs", num_pcs
            
            for delta_idx, delta in enumerate(grid_delta):

                delta_pcs = delta * float(num_pcs)

                print "delta_pcs:", delta_pcs
                #print "delta * num_pc", delta_pcs

                # zero-out eigenvectors of unused PCs
                S_pc = S.copy()
                S_pc[num_pcs:] = 0.0

                # see, e.g. Section 3 of FaST LMM supplement
                D_pc = S_pc + delta_pcs
                
                # precision parameterization (see Bishop, pg. 87)
                A21y = (U_test * (1.0/D_pc)).dot(U_train_y)
                A22 = (U_test * (1.0/D_pc)).dot(U_test.T)

                # perform cholesky
                L = sp.linalg.cho_factor(A22)

                # solve linear system 
                # A22 * y = -A21y
                y_pred_old = -np.linalg.solve(A22, A21y)
                y_pred = -sp.linalg.cho_solve(L, A21y)
                np.testing.assert_array_almost_equal(y_pred_old, y_pred)

                perf[kfold_idx, delta_idx, pc_idx] = mean_squared_error(y_test, y_pred)

            

                # compute out-of-sample log-likelihood
                res = y_test - y_pred
                res_sig = sp.linalg.cho_solve(L, res)

                # compute log determinant from chol_factor
                logdet = -2*np.sum(np.log(np.diag(L[0])))

                # see Carl Rasmussen's book on GPs, equation 5.10, or 
                term1 = -0.5 * logdet
                term2 = -0.5 * sp.dot(res_sig.T, res) # res^2 / sigma2
                term3 = -0.5 * len(res) * sp.log(2 * sp.pi)
                neg_log_likelihood = -(term1 + term2 + term3)
                ll[kfold_idx, delta_idx, pc_idx] = neg_log_likelihood

                """
                # sanity check
                K11 = (U_train * D_pc).dot(U_train.T)
                K11_inv = np.linalg.inv(K11)
                K21 = (U_test * D_pc).dot(U_train.T)
                #K12 = (U_train * D_pc).dot(U_test.T)

                y_pred_cov = K21.dot(K11_inv).dot(y_train)
                np.testing.assert_array_almost_equal(y_pred_cov, y_pred)
                
                #
                X_train = np.ones(len(y_train))
                X_test = np.ones(len(y_test))

                model = fastlmm.getLMM()
                model.setK(K11)
                model.sety(y_train)
                model.setX(X_train)
                
                model.setTestData(Xstar=X_test, K0star=K21)

                # predict on test set
                res = model.nLLeval(delta=0.0, REML=False)
                print "beta", res["beta"]
                out = model.predictMean(beta=res["beta"], delta=0.0)
                perf[kfold_idx, delta_idx, pc_idx] = mean_squared_error(y_test, out)
                #ll_cv1[k_idx, delta_idx] = model.nLLeval_test(fold_data["y_test"], res["beta"], scale=res["sigma2"], delta=delta, Kstar_star=K_test_test)
                """

    return {"perf": perf, "ll": ll, "n_folds": n_folds, "grid_delta": grid_delta, "grid_pcs": grid_pcs}


def perform_selection():

    y = load("autosomes.phen.pickle")
    #y = load("toy.phen.pickle")
    
    print "done loading phenotype, shape", y.shape
    S, U = load("autosomes.eigh.pickle")
    #S, U = load("toy.eigh.pickle")

    print "done loading eig", U.shape

    import time
    t0 = time.time()
    perf = factor(S, U, y)

    #save("toy.pickle", perf)
    save("autosomes.pickle", perf)

    import pylab
    pylab.plot(perf["grid_pcs"], perf["perf"].mean(axis=0).T, "-x", label=perf["grid_delta"])
    pylab.yscale("log")
    pylab.xscale("log")
    pylab.grid(True)
    #pylab.legend()
    pylab.show()
    print "time taken:", time.time()-t0


def load_data():
    """
    perform svd and save to file
    """

    standardizer = stdizer.Unit()

    # set up data
    ##############################
    #
    #bed_reader = Bed("G:\Genetics/dbgap/ARIC/autosomes.genic")
    #heno_fn = "G:\Genetics/dbgap/ARIC/all-ldlsiu02.phe"
    bed_reader = Bed("examples/toydata")
    pheno_fn = "examples/toydata.phe"
     
    # load phenotype
    pheno = plink.loadOnePhen(pheno_fn, 0)
    y = pheno['vals'][:,0]

    print "len unintersected array", len(y)
    
    # load covariates and intersect ids
    indarr = util.intersect_ids([pheno['iid'], bed_reader.original_iids])
    print "len intersected array", len(indarr)

    y = y[indarr[:,0]]
   

    geno = bed_reader.read(order='C')
    G = geno['snps']
    G = standardizer.standardize(G)
    
    G = G[indarr[:,1]]

    print "y.shape", y.shape
    print "G.shape", G.shape

    return G, y


def perform_svd():
    G, y = load_data()
    K = G.dot(G.T)
    eig = np.linalg.eigh(K)
    
    save("toy.eigh.pickle", eig)
    save("toy.phen.pickle", y)

if __name__ == "__main__":
    #result = perform_svd()
    perform_selection()

