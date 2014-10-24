"""
module to perform PCA on genotype data
"""

import sys, os

import numpy as np
import scipy.linalg as LA


#from fastlmm.pyplink.snpreader.Hdf5 import Hdf5
from fastlmm.pyplink.snpreader.Bed import Bed

import fastlmm.feature_selection.PerformSelectionDistributable as dist   
import fastlmm.util.standardizer as stdizer
from fastlmm.util.pickle_io import save


def bed_to_pcs(bed_fn, max_num_pcs, out_fn):
    """load bed file, compute PCs and save as compressed pickle file

    this function assumes that the entire data set fits into memory
    ----------

    bed_fn : str
        File name of binary SNP file

    max_num_pcs : int
        Number of PCs after which we cut

    out_fn : int
        File name of output file

    """

    standardizer = stdizer.Unit()

    bed_reader = Bed(bed_fn)
    geno = bed_reader.read(order='C')
    
    G = geno['snps']
    G = standardizer.standardize(G)

    print "computing K"
    K = G.dot(G.T)
    
    S, U = np.linalg.eigh(K)

    # reduce dimensionality
    S = S[::-1]
    U = U[:,::-1]
    U = U[:,0:max_num_pcs]
    S = S[0:max_num_pcs]

    # save output
    data = {}
    data["iid"] = geno['iid']
    data["U"] = U
    data["S"] = S

    save(out_fn, data)

    """
    pc_rs = ["pc_" + str(i) for i in xrange(max_num_pcs)]
    pc_pos = [[1,0,i] for i in xrange(max_num_pcs)]

    # save as HDF5
    with h5py.File(out_fn, "w") as h5:
        h5.create_dataset('snps', data=X_transform.T, dtype=X_transform.dtype, shuffle=True)
        h5['snps'].attrs["SNP-major"] = True
        h5.create_dataset('iid', data=geno['iid'])
        h5.create_dataset('pos', data=pc_pos)
        h5.create_dataset('rs', data=pc_rs)
    """

#####
# CL's code for simulation experiments below

def getEigvecs_fn(fn,numpcs):
    fnout = "%s_pc%i.vecs"%(fn,numpcs)
    return fnout

def computePC(file, filepath = None, numpc = [5]):
    if filepath is not None:
        fn = os.path.join(filepath,file)
    else:
        fn = file
    if type(numpc) is int or type(numpc) is float:
        numpc = [numpc]
    alt_snpreader = Bed(fn)
    print "computing K"
    K = dist.build_kernel_blocked(fn,alt_snpreader=alt_snpreader)
    print "computing the Eigenvalue decomposition of K"
    [s_all,u_all] = LA.eigh(K)
    s_all=s_all[::-1]
    u_all=u_all[:,::-1]
    for numpcs in numpc:
        #import pdb; pdb.set_trace()
        print "saving %i PCs from %s" %(numpcs,fn)
        
        #import pdb; pdb.set_trace()

        s=s_all[0:numpcs]
        u = u_all[:,0:numpcs]
        outu = np.zeros((u_all.shape[0],numpcs+2),dtype = "|S20")
        outu[:,0:2] = alt_snpreader.original_iids
        outu[:,2::]=u
        fnout = getEigvecs_fn(fn,numpcs)
    
        np.savetxt(fnout,outu,fmt="%s",delimiter = "\t")
        fnout = "%s_pc%i.vals"%(fn,numpcs)
        #outs = np.zeros((s.shape[0],u.shape[1]+2),dtype = "|S20")
        np.savetxt(fnout,s,fmt="%.5f",delimiter = "\t")
    return s_all,u_all


def precompute_aric():
    #filepath = r"\\erg00\Genetics\synthetic\alkes2013\large"
    filepath = r"\\erg00\genetics\dbgap\aric"
    files = [r"autosomes"]

    numpcs = [int(arg) for arg in sys.argv[1:]]

    #files = [r"psz.0",r"fst.0025p.005\psz.0",r"fst.0025p.05\psz.0",r"fst.005p.05\psz.0"]
    #files = [r"fst.0025p.005\psz.0",r"fst.0025p.05\psz.0",r"fst.005p.05\psz.0"]

    for file in files:
        computePC(file, filepath = filepath, numpc = numpcs)


if __name__ == "__main__":


    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # required input
    parser.add_argument('bed_fn', help='input file name of binary snp file', type=str)
    parser.add_argument('max_num_pcs', help='maximal number of pcs to keep', type=int)
    parser.add_argument('out_fn', help='file name of output pickle file', type=str)


    # parse arguments
    args = parser.parse_args()

    bed_to_pcs(args.bed_fn, args.max_num_pcs, args.out_fn)
    
