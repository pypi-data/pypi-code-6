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

__all__ = ['TTmat','eye','randmat']

import numpy as np
from scipy import sparse as scsp
from TensorToolbox.core import TTvec
from TensorToolbox.core import mat_to_tt_idxs

class TTmat(TTvec):
    """ Constructor of multidimensional matrix in Tensor Train format

    :param Candecomp,ndarray,TT A: Available input formats are Candecomp, full tensor in numpy.ndarray, Tensor Train structure (list of cores), list of sparse matrices of sizes (r_{i-1}*r_{i}*nrows x ncols) (used for fast dot product - limited support for other functionalities)
    :param list,int nrows: If int then the row size will be the same in all dimensions, if list then len(nrows) == len(self.TT) (numer of cores) and row size will change for each dimension.
    :param list,int ncols: If int then the column size will be the same in all dimensions, if list then len(ncols) == len(self.TT) (numer of cores) and column size will change for each dimension.
    :param float eps: [default == 1e-8] precision with which to approximate the input tensor
    :param bool is_sparse: [default == False] if True it uses sparsity to accelerate some computations
    :param list sparse_ranks: [default==None] mandatory argument when A is a list of sparse matrices. It contains integers listing the TT-ranks of the matrix.

    .. note:: the method __getitem__ is not overwritten, thus the indices used to access the tensor refer to the flatten versions of the matrices composing the matrix tensor.
    """

    nrows = None
    ncols = None
    is_sparse = None
    sparse_TT = None
    sparse_only = None
    sparse_ranks = None

    def __init__(self,A,nrows,ncols,eps=1e-8,is_sparse=None,sparse_ranks=None):

        self.nrows = []
        self.ncols = []
        self.is_sparse = []
        self.sparse_TT = []
        
        if isinstance(A,list) and np.all( [ isinstance(A[i],scsp.csr_matrix) for i in range(len(A)) ] ):
            if sparse_ranks == None:
                raise AttributeError("The parameter sparse_ranks must be defined for only-sparse initialization")
            
            if len(sparse_ranks) - 1 != len(A):
                raise AttributeError("The condition len(sparse_ranks)-1 == len(A) must hold.")
            
            self.sparse_only = True
            self.sparse_ranks = sparse_ranks
            self.sparse_TT = A

            if isinstance(nrows,int) and isinstance(ncols,int):
                d = len(self.sparse_TT)
                self.nrows = [nrows for i in range(d)]
                self.ncols = [ncols for i in range(d)]
            elif isinstance(nrows,list) and isinstance(ncols,list):
                self.nrows = nrows
                self.ncols = ncols
            else:
                self.init = False
                raise TypeError("tensor.TTmat.__init__: types of nrows and ncols are inconsistent.")

            self.is_sparse = [True] * len(self.sparse_TT)
            self.TT = [None] * len(self.sparse_TT)

            self.init = True

        elif isinstance(A,list) and np.any( [ isinstance(A[i],scsp.csr_matrix) for i in range(len(A)) ] ):
            raise TypeError("Mixed sparse/full initialization not implemented yet")
        else:
            self.sparse_only = False
            TTvec.__init__(self,A,eps)
            if isinstance(nrows,int) and isinstance(ncols,int):
                d = len(self.TT)
                self.nrows = [nrows for i in range(d)]
                self.ncols = [ncols for i in range(d)]
            elif isinstance(nrows,list) and isinstance(ncols,list):
                self.nrows = nrows
                self.ncols = ncols
            else:
                self.init = False
                raise TypeError("tensor.TTmat.__init__: types of nrows and ncols are inconsistent.")
        
            if is_sparse == None:
                self.is_sparse = [False]*len(self.TT)
            elif len(is_sparse) != len(self.TT):
                raise TypeError("tensor.TTmat.__init__: parameter is_sparse must be of length d=A.ndims.")
            else: self.is_sparse = is_sparse

            for i,(is_sp,Ai) in enumerate(zip(self.is_sparse,self.TT)):
                if is_sp:
                    Ai_rsh = np.reshape(Ai,(Ai.shape[0],self.nrows[i],self.ncols[i],Ai.shape[2]))
                    Ai_rsh = np.transpose(Ai_rsh,axes=(0,3,1,2))
                    Ai_rsh = np.reshape(Ai_rsh,(Ai.shape[0]*Ai.shape[2]*self.nrows[i],self.ncols[i]))
                    self.sparse_TT.append( scsp.csr_matrix(Ai_rsh) )
                else:
                    self.sparse_TT.append( None )
        
            # Check that all the mode sizes are equal to rows*cols
            for i,msize in enumerate(self.shape()):
                if msize != self.nrows[i]*self.ncols[i]:
                    self.init = False
                    raise NameError("tensor.TTmat.__init__: the %d-th TT mode size must be equal to nrows[%d]*ncols[%d]" % (i,i,i))

    def copy(self):
        newTT = []
        for TTi in self.TT: newTT.append(TTi.copy())
        return TTmat(newTT,self.nrows,self.ncols,is_sparse=self.is_sparse)

    def kron(self,A):
        if not self.init: raise NameError("tensor.TTmat.extend: TT not initialized correctly")
        if not isinstance(A,TTmat): raise NameError("tensor.TTmat.extend: input tensor is not in TT format")
        if not A.init: raise NameError("tensor.TTmat.extend: input tensor is not initialized correctly")
        self.TT.extend(A.TT)
        self.nrows.extend(A.nrows)
        self.ncols.extend(A.ncols)
        self.is_sparse.extend(A.is_sparse)
        self.sparse_TT.extend(A.sparse_TT)

    def ranks(self):
        if self.sparse_only:
            return self.sparse_ranks
        else:
            return super(TTmat,self).ranks()

    def __getitem__(self,idxs):
        """ 
        Return the item at a certain index. 
        The index is formed as follows:
           idxs = (rowidxs,colidxs) = ((i_1,...,i_d),(j_1,...,j_d))
        """
        if not self.init: raise NameError("tensor.TTmat.__getitem__: TTmat not initialized correctly")
        return TTvec.__getitem__(self,mat_to_tt_idxs(idxs[0],idxs[1],self.nrows,self.ncols))

    def __imul__(A,B):
        if isinstance(A,TTmat) and isinstance(B,TTmat):
            # Check dim consistency
            if A.nrows != B.nrows or A.ncols != B.ncols:
                raise NameError("tensor.multilinalg.mul: Matrices of non consistent dimensions")
        
        return TTvec.__imul__(A,B)


##########################################################
# Constructors of frequently used tensor matrices
##########################################################

# Random rank-1 matrix
def randmat(d,nrows,ncols):
    """ Returns the rank-1 multidimensional random matrix in Tensor Train format
    
    Args:
       d (int): number of dimensions
       nrows (int or list): If int then uniform sizes are used for all the dimensions, if list of int then len(nrows) == d and each dimension will use different size
       ncols (int or list): If int then uniform sizes are used for all the dimensions, if list of int then len(ncols) == d and each dimension will use different size
    
    Returns:
       TTmat The rank-1 multidim random matrix in Tensor Train format
    """
    import numpy.random as npr
    from TensorToolbox.core import Candecomp

    if isinstance(nrows,int): nrows = [ nrows for i in range(d) ]
    if isinstance(ncols,int): ncols = [ ncols for i in range(d) ]
    CPtmp = [npr.random(nrows[i]*ncols[i]).reshape((1,nrows[i]*ncols[i])) + 0.5 for i in range(d)]
    CP_rand = Candecomp(CPtmp)
    TT_rand = TTmat(CP_rand,nrows,ncols)
    return TT_rand

# Identity tensor
def eye(d,N):
    """ Returns the multidimensional identity operator in Tensor Train format
    
    Args:
       d (int): number of dimensions
       N (int or list): If int then uniform sizes are used for all the dimensions, if list of int then len(N) == d and each dimension will use different size
    
    Returns:
       TTmat The multidim identity matrix in Tensor Train format

    Note:
       TODO: improve construction avoiding passage through Candecomp
    """
    from TensorToolbox.core import Candecomp
    if isinstance(N, int):
        If = np.eye(N).flatten().reshape((1,N**2))
        CPtmp = [If for i in range(d)]
    elif isinstance(N, list):
        CPtmp = [np.eye(N[i]).flatten().reshape((1,N[i]**2)) for i in range(d)]
    
    CP_id = Candecomp(CPtmp)
    TT_id = TTmat(CP_id,nrows=N,ncols=N,is_sparse=[True]*d)
    return TT_id

