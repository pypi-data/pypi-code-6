"""
example of how to use feature selection from python (see also command line interface)
"""

import numpy as np
from fastlmm.feature_selection import FeatureSelectionStrategy
from fastlmm.pyplink.snpreader.Bed import Bed
from fastlmm.pyplink.snpreader.Hdf5 import Hdf5

import logging

def runselect(bed_fn=None, pheno_fn=None, strategy=None, select_by_ll=True, output_prefix=None,num_pcs=0, random_state=3, cov_fn=None, k_values=None, delta_values=None,num_folds=10,penalty=0.0):
    logging.basicConfig(level=logging.INFO)


    num_snps_in_memory=200000
	
    # set up data
    ##############################
    bed_fn = Bed("G:\Genetics/dbgap/ARIC/autosomes.genic")
    pheno_fn = "G:\Genetics/dbgap/ARIC/all-ldlsiu02.phe"
    #bed_fn = Bed("examples/toydata")
    #pheno_fn = "examples/toydata.phe"
    pc_fn = "autosomes_pcs.pickle"
    num_pcs_kernel = 20


    # set up grid
    ##############################
    num_steps_delta = 10
    num_steps_k = 8

    # log_2 space and all SNPs
    k_values = np.logspace(0, 12, base=2, num=num_steps_k, endpoint=True).tolist()
    delta_values = np.logspace(-10, 10, endpoint=True, num=num_steps_delta, base=np.exp(1))
    
    mix_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    if strategy is None:
        strategy = 'lmm_full_cv'
        select_by_ll = True
    
    # where to save output
    ##############################
    if output_prefix is None:
        output_prefix = "autosomes"
    
    # go!
    fss = FeatureSelectionStrategy(bed_fn, pheno_fn, num_folds, random_state=random_state, num_pcs=num_pcs, num_pcs_kernel=num_pcs_kernel, num_snps_in_memory=num_snps_in_memory, interpolate_delta=False, cov_fn=cov_fn, pc_fn=pc_fn)

    best_k, best_delta, best_obj, best_snps = fss.perform_selection(k_values, delta_values, mix_values, output_prefix=output_prefix, select_by_ll=select_by_ll, strategy = strategy, penalty=penalty)
    res = {
           'best_k':best_k,
           'best_delta':best_delta,
           'best_obj':best_obj, 
           'best_snps':best_snps
           }
    return res
    

if __name__ == "__main__":
    result = runselect()

