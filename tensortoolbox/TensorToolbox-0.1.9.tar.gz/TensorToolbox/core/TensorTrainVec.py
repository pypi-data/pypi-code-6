#
# This file is part of TensorToolbox.
#
# TensorToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TensorToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with TensorToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

__all__ = ['TTvec','randvec','zerosvec']

import sys
import warnings
import progressbar
import itertools
import copy

import numpy as np
import numpy.random as npr
import numpy.linalg as npla

from scipy import linalg as scla
from scipy import sparse as scsp
from scipy.sparse import linalg as spla

from TensorToolbox.core import ConvergenceError,TTcrossLoopError,\
    TensorWrapper,maxvol,idxfold,idxunfold,ttcross_store, object_store,\
    Candecomp
from TensorToolbox import multilinalg as mla

class TTvec(object):
    """ Constructor of multidimensional tensor in Tensor Train format
        
    :param Candecomp,ndarray,TT A: Available input formats are Candecomp, full tensor in numpy.ndarray, Tensor Train structure (list of cores)
    :param bool generate: whether to perform the construction or just initialize the object
    :param string method: 'svd' use singular value decomposition to construct the TT representation, 'ttcross' use low rank skeleton approximation to construct the TT representation.
    :param float eps: [default == 1e-10] For method=='svd': precision with which to approximate the input tensor. For method=='ttcross': TT-rounding tolerance for rank-check.
    :param list lr_r: list of integer ranks of different cores. If ``None`` then the incremental TTcross approach will be used. (method=='ttcross')
    :param bool lr_fix_rank: determines whether the rank is allowed to be increased (method=='ttcross')
    :param list lr_Jinit: list of list of integers containing the r starting columns in the lowrankapprox routine for each core. If ``None`` then pick them randomly. (method=='ttcross')
    :param float lr_delta: accuracy parameter in the TT-cross routine (method=='ttcross'). It is the relative error in Frobenious norm between two successive iterations.
    :param int lr_maxit: maximum number of iterations in the lowrankapprox routine (method=='ttcross')
    :param float mv_eps: accuracy parameter for each usage of the maxvol algorithm (method=='ttcross')
    :param int mv_maxit: maximum number of iterations in the maxvol routine (method=='ttcross')
    :param bool fix_rank: Whether the rank is allowed to increase
    :param string lr_store_location: Store computed values during construction on the specified file path. The stored values are ttcross_Jinit and the values used in the TensorWrapper. This permits a restart from already computed values. If empty string nothing is done. (method=='ttcross')
    :param string store_object: Object to be stored (default are the tensor wrapper and ttcross_Jinit)
    :param int store_freq: storage frequency. ``store_freq==1`` stores intermediate values at every iteration. The program stores data every ``store_freq`` internal iterations. If ``store_object`` is a SpectralTensorTrain, then ``store_freq`` determines the number of seconds every which to store values.
    
    .. document private functions
    .. automethod:: __getitem__
    """

    A = None                    # Multidimensional data structure
    TT = None
    init = False
    method = 'svd'
    eps = None
    
    # Values only stored for ttcross
    ttcross_rs = None
    ttcross_Js = None
    ttcross_Is = None
    ttcross_Js_last = None
    ttcross_Jinit = None
    ltor_fiber_lists = None
    rtol_fiber_lists = None

    serialize_list = ['TT', 'init', 'method', 'eps', 'ttcross_rs', 'ttcross_Js', 'ttcross_Is', 'ttcross_Js_last', 'ttcross_Jinit', 'ltor_fiber_lists', 'rtol_fiber_lists']

    subserialize_list = ['A']   # Not serialized thanks to the STT interface
    
    def __init__(self,A, eps=1e-10, method='svd', lr_r=None, lr_fix_rank=False, lr_Jinit=None, lr_delta=1e-4, lr_maxit=100, mv_eps=1e-6,mv_maxit=100,lr_store_location="",store_object=None,store_freq=1, generate=True):

        # Initialize the tensor with the input tensor in TT ([][]numpy.ndarray), tensor(numpy.ndarray) or CANDECOMP form
        
        self.A = A
        
        if generate:
            if isinstance(A,Candecomp):
                self.eps = eps
                self.TT = A.to_TT()
                self.init = True
                self.rounding(self.eps)
            elif isinstance(A,np.ndarray) or isinstance(A,TensorWrapper):
                self.eps = eps
                if method == 'svd' or method == None: 
                    self.svd(self.eps)
                    self.method = method
                elif method == 'ttcross': 
                    self.outer_ttcross(self.eps,lr_r,lr_Jinit,lr_delta,lr_maxit,mv_eps,mv_maxit,lr_fix_rank,lr_store_location,store_object,store_freq)
                    self.method = method
                else: raise AttributeError("Method name not recognized. Use 'svd' or 'ttcross'")
            elif isinstance(A,list):
                self.TT = A
                # check consistency just using the ranks function
                self.ranks()
                self.init = True
            else:
                raise NameError("TensorToolbox.TTvec.__init__: Input type not allowed")

    def __getstate__(self):
        dd = dict( [ (tag, getattr( self, tag )) for tag in self.serialize_list ] )
        return dd
    
    def __setstate__(self,state,f = None):
        for tag in state.keys():
            setattr(self, tag, state[tag])
        
    def __getitem__(self,idxs):
        if not self.init: raise NameError("TensorToolbox.TTvec.__getitem__: TT not initialized correctly")
        # TT format: TT[i][idx] = core (matrix or row/col vector)
        if isinstance(idxs,int):
            return self.TT[0][:,idxs,:]
        else:
            out = np.array([1.])
            for i in range(0,len(self.TT)):
                out = np.tensordot(out, self.TT[i][:,idxs[i],:], ( (out.ndim-1,), (0,) ) )
            out = np.tensordot(out,np.array([1.]), ( (out.ndim-1,), (0,) ) )
            return out

    def ranks(self):
        ranks = [1]
        for TTi in self.TT: ranks.append(TTi.shape[2])
        return ranks

    def size(self):
        if not self.init: raise NameError("TensorToolbox.TTvec.size: TT not initialized correctly")
        # TT format: TT[i][idx] = core (matrix or row/col vector)
        tot = 0
        for TTi in self.TT: tot += np.prod(TTi.shape)
        return tot

    def ndim(self):
        if not self.init: raise NameError("TensorToolbox.TTvec.ndim: TT not initialized correctly")
        return len(self.TT)
    
    def shape(self):
        """
        Returns the shape of the tensor represented
        """
        if not self.init: raise NameError("TensorToolbox.TTvec.size: TT not initialized correctly")
        
        s = []
        for TTi in self.TT: s.append(TTi.shape[1])
        return tuple(s)
    
    def to_tensor(self):
        if not self.init: raise NameError("TensorToolbox.TTvec.to_tensor: TT not initialized correctly")
        T = np.array([1.])
        for TTi in self.TT:
            T_ax = T.ndim - 1
            T = np.tensordot(T,TTi,((T_ax,),(0,)))
        T_ax = T.ndim - 1
        T = np.tensordot(T,np.array([1.]),((T_ax,),(0,)))
        return T

    def get_ttcross_eval_idxs(self):
        idxs = []
        dims = self.shape()
        for k in range(len(Is)-1,-1,-1):
            for i in range(len(Is[k])):
                for j in range(len(Js[k])):
                    for kk in range(dims[k]):
                        idxs.append( self.ttcross_Is[k][i] + (kk,) + self.ttcross_Js[k][j] )

        return np.array(idxs)

    def copy(self):
        return copy.deepcopy(self)

    ###########################################
    # Multi-linear Algebra
    ###########################################

    def __add__(A,B):
        C = A.copy()
        C += B
        return C
        
    def __iadd__(A,B):
        """
        In place addition
        """
        if not ( (isinstance(A, TTvec) and A.init) and \
                     ((isinstance(B,TTvec) and B.init) or isinstance(B, float)) ): 
            raise NameError("TensorToolbox.TTvec.add: TT not initialized correctly")

        if isinstance(A,TTvec) and isinstance(B,float):
            lscp = [ np.ones((1,sh)) for i,sh in enumerate(A.shape()) ]
            lscp[0] *= B
            CP = Candecomp( lscp )
            B = TTvec(CP,A.eps)
            if not B.init:
                raise NameError("TensorToolbox.TTvec.add: TT not initialized correctly")
            
        for i in range(len(A.TT)):
            if i == 0:
                A.TT[i] = np.concatenate((A.TT[i],B.TT[i]),axis=2)
            elif i == len(A.TT)-1:
                A.TT[i] = np.concatenate((A.TT[i],B.TT[i]),axis=0)
            else:
                tmpi = np.empty((A.TT[i].shape[0]+B.TT[i].shape[0], A.TT[i].shape[1], A.TT[i].shape[2]+B.TT[i].shape[2]),dtype=np.float64)
                for j in range(A.TT[i].shape[1]): tmpi[:,j,:] = scla.block_diag(A.TT[i][:,j,:],B.TT[i][:,j,:])
                A.TT[i] = tmpi

        return A
    
    def __neg__(A):
        B = -1. * A
        return B

    def __sub__(A,B):
        return A + (-B)
    
    def __isub__(A,B):
        """
        In place subtraction
        """
        A += -B
        return A

    def __div__(A,B):
        if not isinstance(B,float):
            raise AttributeError("TensorToolbox.TTvec.div: Division implemented only for floats")
        return (A * (1./B))
        
    def __mul__(A,B):
        """
        * If A,B are TTvec -> Hadamard product of two TT tensors
        * If A TTvec and B scalar -> multiplication by scalar
        """
        C = A.copy()
        C *= B
        return C
    
    def __rmul__(A,B):
        """
        * If A TTvec and B scalar -> multiplication by scalar
        """
        return (A * B)

    def __imul__(A,B):
        """
        * If A,B are TTvec -> In place Hadamard product
        * If A TTvec and B scalar -> In place multiplication by scalar
        """
        if isinstance(A,TTvec) and isinstance(B,TTvec):
            # Hadamard product
            if not A.init or not B.init:
                raise NameError("TensorToolbox.TTvec.mul: TT not initialized correctly")
            
            if A.shape() != B.shape():
                raise NameError("""TensorToolbox.TTvec.mul: A and B have different shapes\n
                               \t A.shape(): %s
                               \t B.shape(): %s""" % (A.shape(),B.shape()))
            
            for i in range(len(A.TT)):
                tmpi = np.empty((A.TT[i].shape[0]*B.TT[i].shape[0], A.TT[i].shape[1], A.TT[i].shape[2]*B.TT[i].shape[2]), dtype=np.float64)
                for j in range(A.TT[i].shape[1]): tmpi[:,j,:] = np.kron(A.TT[i][:,j,:],B.TT[i][:,j,:])
                A.TT[i] = tmpi
            return A

        elif isinstance(B,float) and isinstance(A,TTvec):
            if not A.init:
                raise NameError("TensorToolbox.TTvec.mul: TT not initialized correctly")

            A.TT[0] *= B
            return A
    
    def __pow__(A,n):
        """
        Power by an integer
        """
        if not A.init:
            raise NameError("TensorToolbox.TTvec.pow: TT not initialized correctly")
        
        if isinstance(n,int):
            B = A.copy()
            for i in range(n-1): B *= A
            return B
        else:
            raise NameError("TensorToolbox.TTvec.pow: n must be an integer")
    
    #########################################
    # Construction
    #########################################
    def svd(self, eps):

        self.eps = eps
        
        """ TT-SVD """
        d = self.A.ndim
        n = self.A.shape
        delta = eps/np.sqrt(d-1) * npla.norm(self.A.flatten(),2) # Truncation parameter
        C = self.A.copy()  # Temporary tensor
        G = []
        if d == 1:
            G.append( C.reshape(1,n[0],1) )
            self.TT = G
            self.init = True
            return
        r = np.empty(d,dtype=int)
        r[0] = 1
        for k in range(d-1):
            C = C.reshape(( r[k]*n[k], C.size/(r[k]*n[k]) ))
            # Compute SVD
            (U,S,V) = npla.svd(C,full_matrices=False)
            # Compute the delta-rank of C
            rk = 0
            Ef = delta + 1.
            while Ef > delta:
                rk += 1
                Ef = npla.norm( C - np.dot(U[:,:rk],scsp.spdiags([S[:rk]],[0],rk,rk).dot(V[:rk,:]) ), ord='fro')
            r[k+1] = rk
            # Generate new core
            G.append( U[:,:r[k+1]].reshape((r[k],n[k],r[k+1])) )
            C = scsp.spdiags([S[:rk]],[0],rk,rk).dot(V[:rk,:])
        G.append(C.reshape(r[k+1],n[k+1],1))
        self.TT = G
        self.init = True


    def outer_ttcross(self, eps, lr_r, lr_Jinit, lr_delta, lr_maxit, mv_eps, mv_maxit, fix_rank = False,lr_store_location="",store_object=None,store_freq=1,multidim_point=None):
        """ Construct a TT representation of A using TT cross. This routine manage the outer loops for incremental ttcross or passes everything to ttcross if lr_r are specified.
        
        :param float eps: tolerance with which to perform the TT-rounding and check the rank accuracy
        :param list lr_r: list of upper ranks (A.ndim)
        :param list lr_Jinit: list (A.ndim-1) of lists of init indices
        :param float lr_delta: TT-cross accuracy
        :param int lr_maxit: maximum number of iterations for ttcross
        :param float mv_eps: MaxVol accuracy
        :param int mv_maxit: maximum number of iterations for MaxVol
        :param bool fix_rank: Whether the rank is allowed to increase
        :param string lr_store_location: Store computed values during construction on the specified file path. The stored values are ttcross_Jinit and the values used in the TensorWrapper. This permits a restart from already computed values. If empty string nothing is done. (method=='ttcross')
        :param string store_object: Object to be stored (default are the tensor wrapper and ttcross_Jinit)
        :param int store_freq: storage frequency. ``store_freq==1`` stores intermediate values at every iteration. The program stores data every ``store_freq`` internal iterations. If ``store_object`` is a SpectralTensorTrain, then ``store_freq`` determines the number of seconds every which to store values.
        :param int multidim_point: If the object A returns a multidimensional array, then this can be used to define which point to apply ttcross to.

        """
        
        import random

        self.eps = eps

        INCREMENTAL = (lr_r == None) or (not fix_rank)
        if not INCREMENTAL:
            try:
                self.ttcross_rs = lr_r
                self.TT = self.ttcross(self.A, lr_r, lr_Jinit, lr_delta, lr_maxit, mv_eps, mv_maxit,lr_store_location=lr_store_location, store_obj=store_obj, store_freq=store_freq, multidim_point=multidim_point)
                self.init = True
            except Exception as e:
                # If the size of the tensor A is small and can be fully stored, store it with also the last Js/Is used in ttcross
                if self.A.size <= 2*1e7/8: # Limit set to approx 20mb of file size
                    import pickle as pkl
                    FILENAME = "TensorToolbox.log"
                    outdic = dict({'A': self.A[tuple([slice(None,None,None) for i in range(d)])],
                                   'Js': self.ttcross_Js,
                                   'Is': self.ttcross_Is,
                                   'Jinit': self.ttcross_Jinit})
                    outfile = open(FILENAME,'wb')
                    pkl.dump(outdic,outfile)
                    outfile.close()
                    print "TTvec: Log file stored"
                raise e

        else:
            from operator import mul

            d = self.A.ndim
            n = self.A.shape
            
            MAXRANK = [ min( reduce(mul,n[:i+1]), reduce(mul,n[i+1:]) ) for i in range(d-1) ]
            MAXRANK.insert(0,1)
            MAXRANK.append(1)
            
            PassedRanks = False
            Js = lr_Jinit

            if lr_r == None:
                r = 2
                self.ttcross_rs = [min( r, MAXRANK[i+1]) for i in range(d-1)]
                self.ttcross_rs.insert(0,1)
                self.ttcross_rs.append(1)
            else:
                self.ttcross_rs = lr_r

            counter = 0
            notpassidxs = None
            while not PassedRanks:
                store_init_Js = (counter == 0)
                counter += 1
                try:
                    Gnew = self.ttcross(self.A,self.ttcross_rs,Js,lr_delta,lr_maxit,mv_eps,mv_maxit,store_init=store_init_Js,lr_store_location=lr_store_location, store_object=store_object,store_freq=store_freq, multidim_point=multidim_point)
                except TTcrossLoopError as e:
                    # If a loop is detected, then ask for a rank increase
                    print "Loop detected! Increasing ranks."
                    PassedRanks = False
                    if notpassidxs == None: notpassidxs = range(d-1) # If this is the first run, mark all as not passed
                    notpassidxs_old = notpassidxs[:]
                    notpassidxs = []
                    for i in range(1,d):
                        if ((i-1) in notpassidxs_old) and (not self.ttcross_rs[i] == MAXRANK[i]):
                            self.ttcross_rs[i] += 1
                            notpassidxs.append(i-1)
                except ConvergenceError as e:
                    # If the ttcross reaches the maximum number of function iterations,
                    # increase the ranks like for TTcrossLoopError
                    print "ttcross not converged, maximum num. of iterations reached. Increasing ranks"
                    PassedRanks = False
                    if notpassidxs == None: notpassidxs = range(d-1) # If this is the first run, mark all as not passed
                    notpassidxs_old = notpassidxs[:]
                    notpassidxs = []
                    for i in range(1,d):
                        if ((i-1) in notpassidxs_old) and (not self.ttcross_rs[i] == MAXRANK[i]):
                            self.ttcross_rs[i] += 1
                            notpassidxs.append(i-1)
                except:
                    # For big problems, even with small dimensionality, this logging is unpractical
                    # # If the size of the tensor A is small and can be fully stored, store it with also the last Js/Is used in ttcross
                    # if self.A.size <= 2*1e7/8: # Limit set to approx 20mb of file size
                    #     import pickle as pkl
                    #     FILENAME = "TensorToolbox.log"
                    #     outdic = dict({'A': self.A[tuple([slice(None,None,None) for i in range(d)])],
                    #                    'Js': self.ttcross_Js,
                    #                    'Is': self.ttcross_Is,
                    #                    'Jinit': self.ttcross_Jinit})
                    #     outfile = open(FILENAME,'wb')
                    #     pkl.dump(outdic,outfile)
                    #     outfile.close()
                    #     print "TTvec: Log file stored"
                    raise
                else:
                    TTapprox = TTvec( Gnew )

                    crossRanks = TTapprox.ranks()
                    roundRanks = TTapprox.rounding(eps).ranks()
                    PassedRanks = True
                    notpassidxs = []
                    for i in range(1,d):
                        if not (crossRanks[i] > roundRanks[i] or roundRanks[i] == MAXRANK[i]):
                            notpassidxs.append(i-1) # i-1 because Js[0] is referred already to the first core
                            self.ttcross_rs[i] += 1
                            PassedRanks = False 
                
                Js_old = self.ttcross_Js
                Js = []
                if not PassedRanks:
                    
                    # Get last indices used copy them
                    for i in range(len(Js_old)):
                        Js.append( Js_old[i][:] )
                        
                    # Get last indices and augment them with one entry (possibly already computed)
                    for i in notpassidxs:
                        newidx = Js[i][0]
                        # Try first with already computed indices looking to all the history of Js
                        jtmp = len(self.ttcross_Js_last)-1
                        while (newidx in Js[i]) and jtmp >= 0 :
                            Js_tmp = self.ttcross_Js_last[jtmp]
                            Js_diff = set(Js_tmp[i]) - set(Js[i])
                            if len( Js_diff ) > 0:
                                # pick one randomly in the diff
                                newidx = random.sample(Js_diff,1)[0]
                            jtmp -= 1
                        
                        # Pick randomly if none was found in previously computed sequence
                        while newidx in Js[i]: newidx = tuple( [random.choice(range(n[j])) for j in range(i+1,d)] )
                        Js[i].append(newidx)
            
            self.TT = Gnew
            self.init = True

    def ttcross(self, A, lr_r, lr_Jinit, lr_delta, lr_maxit, mv_eps, mv_maxit, store_init=True,lr_store_location="",store_object=None,store_freq=1,multidim_point=None):
        """ Construct a TT representation of A using TT cross
        
        :param nd.array/TensorWrapper A: 
        :param list lr_r: list of upper ranks (A.ndim)
        :param list lr_Jinit: list (A.ndim-1) of lists of init indices
        :param string lr_store_location: Store computed values during construction on the specified file path. The stored values are ttcross_Jinit and the values used in the TensorWrapper. This permits a restart from already computed values. If empty string nothing is done. (method=='ttcross')
        :param string store_object: Object to be stored (default are the tensor wrapper and ttcross_Jinit)
        :param int store_freq: storage frequency. ``store_freq==1`` stores intermediate values at every iteration. The program stores data every ``store_freq`` internal iterations. If ``store_object`` is a SpectralTensorTrain, then ``store_freq`` determines the number of seconds every which to store values.
        :param int multidim_point: If the object A returns a multidimensional array, then this can be used to define which point to apply ttcross to.

        """
        
        import random
        import operator
        from TensorToolbox.core import STT

        self.ttcross_Js_last = []
        
        d = A.ndim
        n = A.shape
        
        if len(lr_r) != d+1:
            raise AttributeError("List of guessed ranks must be of length A.ndim")
        
        if lr_r[0] != 1 or lr_r[-1] != 1:
            raise ValueError("r[0] and r[-1] must be 1")
        
        if lr_Jinit == None: lr_Jinit = [None for i in range(d)]

        if len(lr_Jinit) != d:
            raise AttributeError("List of init indexes must be of length A.ndim-1")
        for k_Js in range(len(lr_Jinit)-1):
            if lr_Jinit[k_Js] == None:
                if lr_r[k_Js+1] > max( np.prod(n[k_Js+1:]), sys.maxint ):
                    raise ValueError("Ranks selected exceed the dimension of the tensor")
                
                # Lazy selection of indices... this can be done better.
                lr_Jinit[k_Js] = []
                for i in range(lr_r[k_Js+1]):
                    newidx = tuple( [ random.choice(range(n[j])) for j in range(k_Js+1,d) ] )
                    while newidx in lr_Jinit[k_Js]:
                        newidx = tuple( [ random.choice(range(n[j])) for j in range(k_Js+1,d) ] )
                    
                    lr_Jinit[k_Js].append(newidx)

            if len(lr_Jinit[k_Js]) != lr_r[k_Js+1]:
                raise ValueError("Lenght of init right sequence must agree with the upper rank values #1")
            for idx in lr_Jinit[k_Js]:
                if len(idx) != d - (k_Js + 1):
                    raise ValueError("Lenght of init right sequence must agree with the upper rank values #2")
        
        if lr_Jinit[-1] == None: lr_Jinit[-1] = [()]

        if store_init: self.ttcross_Jinit = lr_Jinit
        
        Gold = [ np.zeros((lr_r[k],n[k],lr_r[k+1])) for k in range(d) ]
        Gnew = [ npr.random((lr_r[k],n[k],lr_r[k+1])) for k in range(d) ]
        
        # Normalize Gnew so that we enter the first loop and check for inf or 0. value
        tt_Gnew = TTvec(Gnew)
        fro_new = mla.norm(tt_Gnew,'fro')
        if fro_new == np.inf or fro_new == 0.:
            raise OverflowError("TensorToolbox.TensorTrainVec: The Frobenious norm of the init TT is: %f" % fro_new )
        tt_Gnew = tt_Gnew * (1./fro_new)
        Gnew = tt_Gnew.TT
        
        Js = lr_Jinit

        self.ltor_fiber_lists = []
        self.rtol_fiber_lists = []
        lr_it = 0
        store_counter = 0
        while lr_it < lr_maxit and mla.norm(TTvec(Gold)-TTvec(Gnew),'fro') > lr_delta * mla.norm(TTvec(Gnew), 'fro'):
            lr_it += 1
            if isinstance(A,TensorWrapper) and A.twtype == 'array':
                try:
                    totsize = float(A.get_size())
                    sys.stdout.write("Ranks: %s - Iter: %d - Fill: %e%%\r" % (str(lr_r),lr_it , float(A.get_fill_level())/totsize * 100.) )
                except OverflowError:
                    sys.stdout.write("Ranks: %s - Iter: %d - Fill: %d\r" % (str(lr_r),lr_it , A.get_fill_level()) )
            else:
                sys.stdout.write("Ranks: %s - Iter: %d \r" % (str(lr_r),lr_it) )
            sys.stdout.flush()

            Gold = Gnew
            Gnew = [None for i in range(d)]
            
            ######################################
            # left-to-right step
            ltor_fiber_list = []
            Is = [[()]]
            for k in range(d-1):
                if isinstance(A,TensorWrapper) and A.twtype == 'array':
                    try:
                        totsize = float(A.get_size())
                        sys.stdout.write("Ranks: %s - Iter: %d - LR: %d - Fill: %e%%\r" % (str(lr_r),lr_it,k, float(A.get_fill_level())/totsize * 100.) )
                    except OverflowError:
                        sys.stdout.write("Ranks: %s - Iter: %d - LR: %d - Fill: %d\r" % (str(lr_r),lr_it,k, A.get_fill_level()) )
                else:
                    sys.stdout.write("Ranks: %s - Iter: %d - LR: %d \r" % (str(lr_r),lr_it,k))
                sys.stdout.flush()

                # Extract fibers
                for i in range(lr_r[k]):
                    for j in range(lr_r[k+1]):
                        fiber = Is[k][i] + (slice(None,None,None),) + Js[k][j]
                        ltor_fiber_list.append(fiber)
                
                if k == 0:      # Is[k] will be empty
                    idx = (slice(None,None,None),) + tuple(itertools.izip(*Js[k]))
                else:
                    it = itertools.product(Is[k],Js[k])
                    idx = [ [] for i in range(d) ]
                    for (lidx,ridx) in it:
                        for j,jj in enumerate(lidx): idx[j].append(jj)
                        for j,jj in enumerate(ridx): idx[len(lidx)+1+j].append(jj)
                    idx[k] = slice(None,None,None)
                    idx = tuple(idx)
                
                if multidim_point == None:
                    C = A[ idx ]
                else:
                    C = np.asarray(A[ idx ].tolist())\
                        [(slice(None,None,None),slice(None,None,None)) + multidim_point]
                
                if k == 0:
                    C = C.reshape(n[k], lr_r[k], lr_r[k+1])
                    C = C.transpose( (1,0,2) )
                else:
                    C = C.reshape(lr_r[k], lr_r[k+1], n[k])
                    C = C.transpose( (0,2,1) )
                                
                C = C.reshape(( lr_r[k] * n[k], lr_r[k+1] ))

                # Compute QR decomposition
                (Q,R) = scla.qr(C,mode='economic')
                # Maxvol
                (I,QsqInv,it) = maxvol(Q,mv_eps,mv_maxit)

                # Retrive indices in folded tensor
                IC = [ idxfold( [lr_r[k],n[k]], idx ) for idx in I ] # First retrive idx in folded C
                IT = [ Is[k][ic[0]] + (ic[1],) for ic in IC ] # Then reconstruct the idx in the tensor
                Is.append(IT)

            # end left-to-right step
            ###############################################

            # Store last Js indices (for restarting purposes)
            self.ttcross_Js_last.append([ J[:] for J in Js ])
            
            #####################################
            # right-to-left step
            rtol_fiber_list = []
            Js = [None for i in range(d)]
            Js[-1] = [()]
            for k in range(d,1,-1):
                if isinstance(A,TensorWrapper) and A.twtype == 'array':
                    try:
                        totsize = float(A.get_size())
                        sys.stdout.write("Ranks: %s - Iter: %d - RL: %d - Fill: %e%%\r" % (str(lr_r),lr_it,k, float(A.get_fill_level())/totsize * 100.) )
                    except OverflowError:
                        sys.stdout.write("Ranks: %s - Iter: %d - RL: %d - Fill: %d\r" % (str(lr_r),lr_it,k, A.get_fill_level()) )
                else:
                    sys.stdout.write("Ranks: %s - Iter: %d - RL: %d \r" % (str(lr_r),lr_it,k))
                sys.stdout.flush()

                # Extract fibers
                for i in range(lr_r[k-1]):
                    for j in range(lr_r[k]):
                        fiber = Is[k-1][i] + (slice(None,None,None),) + Js[k-1][j]
                        rtol_fiber_list.append(fiber)
                
                if k == d:      # Is[k] will be empty
                    idx = tuple(itertools.izip(*Is[k-1])) + (slice(None,None,None),)
                else:
                    it = itertools.product(Is[k-1],Js[k-1])
                    idx = [ [] for i in range(d) ]
                    for (lidx,ridx) in it:
                        for j,jj in enumerate(lidx): idx[j].append(jj)
                        for j,jj in enumerate(ridx): idx[len(lidx)+1+j].append(jj)
                    idx[k-1] = slice(None,None,None)
                    idx = tuple(idx)
                
                if multidim_point == None:
                    C = A[ idx ]
                else:
                    C = np.asarray(A[ idx ].tolist())\
                        [(slice(None,None,None),slice(None,None,None)) + multidim_point]
                
                C = C.reshape(lr_r[k-1], lr_r[k], n[k-1])
                C = C.transpose( (0,2,1) )
                
                C = C.reshape( (lr_r[k-1],n[k-1]*lr_r[k]) ).T
                
                # Compute QR decomposition
                (Q,R) = scla.qr(C,mode='economic')
                # Maxvol
                (J,QsqInv,it) = maxvol(Q,mv_eps,mv_maxit)
                
                # Retrive indices in folded tensor
                JC = [ idxfold( [n[k-1],lr_r[k]], idx ) for idx in J ] # First retrive idx in folded C
                JT = [  (jc[0],) + Js[k-1][jc[1]] for jc in JC ] # Then reconstruct the idx in the tensor
                Js[k-2] = JT
                
                # Compute core
                Gnew[k-1] = np.dot(Q,QsqInv).T.reshape( (lr_r[k-1], n[k-1], lr_r[k]) )
            
            # Check that none of the previous iteration has already used the same fibers 
            # (this indicates the presence of a loop). 
            # If this is the case apply a random perturbation on one of the fibers
            loop_detected = False
            i = 0
            while (not loop_detected) and i < len(self.rtol_fiber_lists)-1:
                loop_detected = all(map( operator.eq, self.rtol_fiber_lists[i], rtol_fiber_list )) \
                    and all(map( operator.eq, self.ltor_fiber_lists[i], ltor_fiber_list ))
                i += 1
            
            if loop_detected:# and rtol_loop_detected:
                # If loop is detected, then an exception is raised
                # and the outer_ttcross will increase the rank
                self.ttcross_Js = Js
                self.ttcross_Is = Is
                sys.stdout.write("\n")
                sys.stdout.flush()
                raise TTcrossLoopError('Loop detected!')
            else:
                self.ltor_fiber_lists.append(ltor_fiber_list)
                self.rtol_fiber_lists.append(rtol_fiber_list)
            
            # Add the last core
            idx = (slice(None,None,None),) + tuple(itertools.izip(*Js[0]))
            if multidim_point == None:
                C = A[ idx ]
            else:
                C = np.asarray(A[ idx ].tolist())\
                    [(slice(None,None,None),slice(None,None,None)) + multidim_point]
            
            C = C.reshape(n[0], 1, lr_r[1])
            C = C.transpose( (1,0,2) )
            
            Gnew[0] = C 

        sys.stdout.write("\n")
        sys.stdout.flush()

        if lr_it >= lr_maxit:
            self.ttcross_Js = Js
            self.ttcross_Is = Is
            raise ConvergenceError('Maximum number of iteration reached.')

        if mla.norm(TTvec(Gold)-TTvec(Gnew),'fro') > lr_delta * mla.norm(TTvec(Gnew), 'fro'):
            self.ttcross_Js = Js
            self.ttcross_Is = Is
            raise ConvergenceError('Low Rank Approximation algorithm did not converge.')
        
        self.ttcross_Js = Js
        self.ttcross_Is = Is

        # Final storage
        if lr_store_location != None and \
                lr_store_location != "":
            if store_object == None:
                ttcross_store(lr_store_location,A,self)
            elif isinstance(store_object,STT):
                if store_object.to_be_stored(): object_store(lr_store_location,store_object)
            else:
                object_store(lr_store_location,store_object)
        
        return Gnew
        
    def kron(self,A):
        if not self.init: raise NameError("TensorToolbox.TTvec.extend: TT not initialized correctly")
        if not isinstance(A,TTvec): raise NameError("TensorToolbox.TTvec.extend: input tensor is not in TT format")
        if not A.init: raise NameError("TensorToolbox.TTvec.extend: input tensor is not initialized correctly")
        self.TT.extend(A.TT)

    def rounding2(self,eps,show_progress=False):
        if not self.init: raise NameError("TensorToolbox.TTvec.rounding: TT not initialized correctly")
        """ TT-rounding """
        d = len(self.TT)
        n = self.shape()
        r = self.ranks()
        nrm = np.zeros(d,dtype=np.float64)
        core0 = self.TT[0]
        if show_progress:
            bar = progressbar.ProgressBar(maxval=d-1,
                                          widgets=[progressbar.Bar(
                        '=', '[TensorToolbox.TTvec] Rounding - Left-right orth. [', ']'), ' ', progressbar.Percentage()])
            bar.start()
        for i in range(d-1):
            if show_progress:
                bar.update(i)
            core0 = np.reshape(core0,(r[i]*n[i],r[i+1]))
            (core0,ru) = scla.qr(core0,mode='economic')
            nrm[i+1] = npla.norm(ru,'fro')
            ru /= max(nrm[i+1],1e-300)
            core1 = self.TT[i+1].reshape((r[i+1],n[i+1]*r[i+2]))
            core1 = np.dot(ru,core1)
            r[i+1] = core0.shape[1]
            self.TT[i] = np.reshape(core0,(r[i],n[i],r[i+1]))
            self.TT[i+1] = np.reshape(core1,(r[i+1],n[i+1],r[i+2]))
            core0 = core1

        if show_progress:
            bar.finish()
        
        ep = eps/np.sqrt(d-1)
        core0 = self.TT[d-1]
        if show_progress:
            bar = progressbar.ProgressBar(maxval=d-1,
                                          widgets=[progressbar.Bar(
                        '=', '[TensorToolbox.TTvec] Rounding - Right-left svd [', ']'), ' ', progressbar.Percentage()])
            bar.start()
        for i in range(d-1,0,-1):
            if show_progress:
                bar.update(d-i)
            core1 = self.TT[i-1].reshape((r[i-1]*n[i-1],r[i]))
            core0 = np.reshape(core0,(r[i],n[i]*r[i+1]))
            (U,S,V) = scla.svd(core0,full_matrices=False)
            r1 = self.__round_chop(S,npla.norm(S,2)*ep)            # Truncate
            U = U[:,:r1]
            S = S[:r1]
            V = V[:r1,:]
            U = np.dot(U,np.diag(S))
            r[i] = r1
            core1 = np.dot(core1,U)
            self.TT[i] = np.reshape(V,(r[i],n[i],r[i+1]))
            self.TT[i-1] = np.reshape(core1,(r[i-1],n[i-1],r[i]))
            core0 = core1.copy()
        
        if show_progress:
            bar.finish()

        pp = self.TT[0]
        nrm[0] = np.sqrt(np.sum(pp**2.))
        if np.abs(nrm[0]) > np.spacing(1):
            self.TT[0] /= nrm[0]
        # Ivan's trick to redistribute norms
        nrm0 = np.sum(np.log(np.abs(nrm)))
        nrm0 = nrm0/float(d)
        nrm0 = np.exp(nrm0)
        if nrm0 > np.spacing(1):
            for i in range(d-1):
                nrm[i+1] = nrm[i+1]*nrm[i]/nrm0
                nrm[i] = nrm0
        # Redistribute norm
        for i in range(d): self.TT[i] *= nrm[i]
        
        return self

    def __round_chop(self,S,eps):
        ss = np.cumsum(S[::-1]**2.)
        return len(S) - next(i for i,s in enumerate(ss) if s > eps**2. or i == len(S)-1)

    def rounding(self,eps,show_progress=False):
        if not self.init: raise NameError("TensorToolbox.TTvec.rounding: TT not initialized correctly")

        """ TT-rounding """
        d = len(self.TT)
        ns = self.shape()

        # OBS: The truncation parameter could be computed during the right to left orthogonalization?
        delta = eps/np.sqrt(d-1) # Truncation parameter

        # Right to left orthogonalization
        nrm = np.zeros(d,dtype=np.float64)
        if show_progress:
            bar = progressbar.ProgressBar(maxval=d-1,
                                          widgets=[progressbar.Bar(
                        '=', '[TensorToolbox.TTvec] Rounding - Right-left orth. [', ']'), ' ', progressbar.Percentage()])
            bar.start()
        for k in range(d-1,0,-1):
            if show_progress:
                bar.update(d-k)
            # Computation of rq components
            alphakm1 = self.TT[k].shape[0]
            betak = self.TT[k].shape[2]
            Gk = np.reshape(self.TT[k],(alphakm1,self.TT[k].shape[1]*betak))
            (R,Q) = scla.rq(Gk,mode='economic')
            nrm[k-1] = npla.norm(R,'fro')
            betakm1 = R.shape[1]
            R /= max(nrm[k-1],1e-300)
            self.TT[k] = np.reshape(Q,(betakm1,self.TT[k].shape[1],betak))
            # 3-mode product G[k-1] x_3 R 
            C = self.TT[k-1].reshape((self.TT[k-1].shape[0]*self.TT[k-1].shape[1],self.TT[k-1].shape[2]))
            self.TT[k-1] = np.dot(C,R).reshape((self.TT[k-1].shape[0],self.TT[k-1].shape[1],betakm1))
            # gc.collect()

        if show_progress:
            bar.finish()
        
        # Compression
        r = [1]
        if show_progress:
            bar = progressbar.ProgressBar(maxval=d-1,
                                          widgets=[progressbar.Bar(
                        '=', '[TensorToolbox.TTvec] Rounding - Left-right svd [', ']'), ' ', progressbar.Percentage()])
            bar.start()
        for k in range(d-1):
            if show_progress:
                bar.update(k)
            C = self.TT[k].copy().reshape((self.TT[k].shape[0]*self.TT[k].shape[1],self.TT[k].shape[2]))
            # Compute SVD
            (U,S,V) = npla.svd(C,full_matrices=False)
            # Truncate SVD
            rk = 0
            rk = self.__round_chop(S,npla.norm(S,2)*delta)            # Truncate

            r.append( rk )
            self.TT[k] = U[:,:r[k+1]].reshape((r[k],self.TT[k].shape[1],r[k+1]))
            # Update next core with 1-mode product.
            SV = np.tile(S[:r[k+1]],(V.shape[1],1)).T * V[:r[k+1],:]
            C = self.TT[k+1].reshape((self.TT[k+1].shape[0], self.TT[k+1].shape[1]*self.TT[k+1].shape[2]))
            self.TT[k+1] = np.dot(SV,C).reshape((r[k+1],ns[k+1],self.TT[k+1].shape[2]))
            # gc.collect()

        if show_progress:
            bar.finish()
        
        nrm[d-1] = npla.norm(self.TT[d-1].flatten(),2)
        self.TT[d-1] /= max(nrm[d-1],1e-300)

        # Oseledets Trick here!
        nrm0 = np.sum(np.log(np.abs(nrm)))
        nrm0 = nrm0/float(d)
        nrm0 = np.exp(nrm0)
        if np.abs(nrm0) > np.spacing(1):
            # Construct normalization of norm
            for i in range(d-1,0,-1):
                nrm[i-1] = nrm[i-1]*nrm[i]/nrm0
                nrm[i] = nrm0

        # Redistribute the norm
        for i in range(d-1,-1,-1): self.TT[i] *= nrm[i]
        
        return self

    def interpolate(self,Ms=None,eps=1e-8,is_sparse=None):
        """ Interpolates the values of the TTvec at arbitrary points, using the interpolation matrices ``Ms''.
        
        :param list Ms: list of interpolation matrices for each dimension. Ms[i].shape[1] == self.shape()[i]
        :param float eps: tolerance with which to perform the rounding after interpolation
        :param list is_sparse: is_sparse[i] is a bool indicating whether Ms[i] is sparse or not. If 'None' all matrices are non sparse
        
        :returns: TTvec interpolation
        :rtype: TTvec

        >>> from DABISpectralToolbox import DABISpectral1D as S1D
        >>> Ms = [ S1D.LinearInterpolationMatrix(X[i],XI[i]) for i in range(d) ]
        >>> is_sparse = [True]*d
        >>> TTapproxI = TTapprox.interpolate(Ms,eps=1e-8,is_sparse=is_sparse)
        """
        from TensorToolbox import TTmat

        if not self.init: raise NameError("TensorToolbox.TTvec.project: TT not initialized correctly")
        
        if len(Ms) != self.ndim():
            raise AttributeError("The length of Ms and the dimension of the TTvec must be the same!")

        d = len(Ms)
        for i in range(d):
            if Ms[i].shape[1] != self.shape()[i]:
                raise AttributeError("The condition  Ms[i].shape[1] == self.shape()[i] must hold.")                        

        if isinstance(Ms,list) and np.all( [ isinstance(Ms[i],scsp.csr_matrix) for i in range(len(Ms)) ] ):
            sparse_ranks = [1] * (d+1)
            nrows = [Ms[i].shape[0] for i in range(d)]
            ncols = [Ms[i].shape[1] for i in range(d)]
            TT_MND = TTmat(Ms, nrows, ncols, sparse_ranks=sparse_ranks)
        else:
            if is_sparse == None: is_sparse = [False]*len(Ms)

            # Construct the interpolating TTmat
            TT_MND = TTmat(Ms[0].flatten(),nrows=Ms[0].shape[0],ncols=Ms[0].shape[1],is_sparse=[ is_sparse[0] ])
            for M,s in zip(Ms[1:],is_sparse[1:]):
                TT_MND.kron( TTmat(M.flatten(),nrows=M.shape[0],ncols=M.shape[1],is_sparse=[s]) )
        
        # Perform interpolation
        return mla.dot(TT_MND,self).rounding(eps)
    
    def project(self, Vs=None, Ws=None, eps=1e-8,is_sparse=None):
        """ Project the TTvec onto a set of basis provided, using the Generalized Vandermonde matrices ``Vs'' and weights ``Ws''.
        
        :param list Vs: list of generalized Vandermonde matrices for each dimension. Ms[i].shape[1] == self.shape()[i]
        :param list Ws: list of weights for each dimension. Ws[i].shape[0] == self.shape()[i]
        :param float eps: tolerance with which to perform the rounding after interpolation
        :param list is_sparse: is_sparse[i] is a bool indicating whether Ms[i] is sparse or not. If 'None' all matrices are non sparse
        
        :returns: TTvec containting the Fourier coefficients
        :rtype: TTvec

        >>> from DABISpectralToolbox import DABISpectral1D as S1D
        >>> P = S1D.Poly1D(S1D.JACOBI,(0,0))
        >>> x,w = S1D.Quadrature(10,S1D.GAUSS)
        >>> X = [x]*d
        >>> W = [w]*d
        >>> # Compute here the TTapprox at points X
        >>> TTapprox = TTvec(....)
        >>> # Project
        >>> Vs = [ P.GradVandermonde1D(x,10,0,norm=False) ] * d
        >>> is_sparse = [False]*d
        >>> TTfourier = TTapprox.project(Vs,W,eps=1e-8,is_sparse=is_sparse)
        """
        from TensorToolbox import TTmat
        
        if not self.init: raise NameError("TensorToolbox.TTvec.project: TT not initialized correctly")
        
        if len(Vs) != len(Ws) or len(Ws) != self.ndim():
            raise AttributeError("The length of Vs, Ms and the dimension of the TTvec must be the same!")

        d = len(Vs)
        for i in range(d):
            if Vs[i].shape[1] != Ws[i].shape[0] or Ws[i].shape[0] != self.shape()[i]:
                raise AttributeError("The condition  Vs[i].shape[1] == Ws[i].shape[0] == self.shape()[i] must hold.")                

        if is_sparse == None: is_sparse = [False]*d
        
        # Prepare matrices
        VV = [ Vs[i].T * np.tile(Ws[i],(Vs[i].shape[0],1)) for i in range(d) ]

        TT_MND = TTmat(VV[0].flatten(),nrows=VV[0].shape[0],ncols=VV[0].shape[1],is_sparse=[ is_sparse[0] ])
        for V,s in zip(VV[1:],is_sparse[1:]):
            TT_MND.kron( TTmat(V.flatten(),nrows=V.shape[0],ncols=V.shape[1],is_sparse=[s]) )
        
        # Perform projection
        return mla.dot(TT_MND,self).rounding(eps)

##########################################################
# Constructors of frequently used tensor vectors
##########################################################

def randvec(d,N):
    """ Returns the rank-1 multidimensional random vector in Tensor Train format
    
    Args:
       d (int): number of dimensions
       N (int or list): If int then uniform sizes are used for all the dimensions, if list of int then len(N) == d and each dimension will use different size
    
    Returns:
       TTvec The rank-1 multidim random vector in Tensor Train format
    """
    import numpy.random as npr
    from TensorToolbox.core import Candecomp

    if isinstance(N,int):
        N = [ N for i in range(d) ]
    CPtmp = [npr.random(N[i]).reshape((1,N[i])) + 0.5 for i in range(d)]
    CP_rand = Candecomp(CPtmp)
    TT_rand = TTvec(CP_rand)
    return TT_rand

def zerosvec(d,N):
    """ Returns the rank-1 multidimensional vector of zeros in Tensor Train format
    
    Args:
       d (int): number of dimensions
       N (int or list): If int then uniform sizes are used for all the dimensions, if list of int then len(N) == d and each dimension will use different size
    
    Returns:
       TTvec The rank-1 multidim vector of zeros in Tensor Train format
    """
    from TensorToolbox.core import Candecomp

    if isinstance(N,int):
        N = [ N for i in range(d) ]
    CPtmp = [np.zeros((1,N[i])) for i in range(d)]
    CP_zeros = Candecomp(CPtmp)
    TT_zeros = TTvec(CP_zeros)
    return TT_zeros

def onesvec(d,N):
    """ Returns the rank-1 multidimensional vector of ones in Tensor Train format
    
    Args:
       d (int): number of dimensions
       N (int or list): If int then uniform sizes are used for all the dimensions, if list of int then len(N) == d and each dimension will use different size
    
    Returns:
       TTvec The rank-1 multidim vector of ones in Tensor Train format
    """
    from TensorToolbox.core import Candecomp

    if isinstance(N,int):
        N = [ N for i in range(d) ]
    CPtmp = [np.ones((1,N[i])) for i in range(d)]
    CP_rand = Candecomp(CPtmp)
    TT_rand = TTvec(CP_rand)
    return TT_rand
