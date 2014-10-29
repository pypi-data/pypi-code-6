#!/usr/bin/env python2.7
#
# Written (W) 2014 Christian Widmer
# Copyright (C) 2014 Microsoft Research

"""
Created on 2014-03-19
@author: Christian Widmer
@summary: Linear Mix Model that caches computations using joblib
"""

import numpy.linalg as la
import numpy as np

import logging
from sklearn.externals import joblib
from fastlmm.inference import LMM


class CachedLMM(LMM):
    '''
    wrapper around lmm that caches all possible computations
    '''
    
    def __init__(self, cachedir, forcefullrank=False, min_size=1000):
        '''
        Input:
        cachedir        : str, directory where to cache results
        forcefullrank   : if True, then the code always computes K and runs cubically (False)
        min_size        : int, min size of linear algebra operations for which to perform caching
        '''

        super(CachedLMM, self).__init__(forcefullrank=forcefullrank)

        if cachedir == None:
            logging.warn("no caching path provided, using non-cached LMM")
        else:
            logging.debug("caching to dir %s" % cachedir)
            self.mem = joblib.Memory(cachedir=cachedir, verbose=True, compress=True)
            #mem.clear()
            #print mem
            
            self.cached_eigh = self.mem.cache(la.eigh)
            self.cached_svd = self.mem.cache(la.svd)
            self.cached_dot = self.mem.cache(np.dot)
            
            def wrapped_eigh(A, **kwargs):
                if min(A.shape) < min_size:
                    logging.debug("shape too small for caching, using regular eigh")
                    return la.eigh(A, **kwargs)
                else:
                    logging.debug("using cached eigh")
                    return self.cached_eigh(A, **kwargs)
                            
            def wrapped_svd(A, **kwargs):
                if min(A.shape) < min_size:
                    logging.debug("shape too small for caching, using regular svd")
                    return la.svd(A, **kwargs)
                else:
                    logging.debug("using cached svd")
                    return self.cached_svd(A, **kwargs)
            
            def wrapped_dot(A, B, **kwargs):
                if min(A.shape) < min_size or min(B.shape) < min_size:
                    logging.debug("shape too small for caching, using regular dot")
                    return np.dot(A, B, **kwargs)
                else:
                    logging.debug("using cached dot")
                    return self.cached_dot(A, B, **kwargs)
                           
            # extract certain operations for caching
            self.svd = wrapped_svd
            self.eigh = wrapped_eigh
            self.dot = wrapped_dot
            
