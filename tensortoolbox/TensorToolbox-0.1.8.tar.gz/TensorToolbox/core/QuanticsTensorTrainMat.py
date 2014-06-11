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

__all__ = ['QTTmat']

import operator
import numpy as np
from TensorToolbox.core import QTTvec
from TensorToolbox.core import TTmat
from TensorToolbox.core import idxfold, idxunfold

class QTTmat(TTmat):
    """ Constructor of multidimensional matrix in Quantics Tensor Train format

    :param ndarray,TT A: Available input formats are full tensor in numpy.ndarray, Tensor Train structure (list of cores). If input is ndarray, then it must be in mattensor format (see aux.py)
    :param int base: folding base for QTT representation
    :param int nrows: If int then the row size will be the same in all dimensions, if list then len(nrows) == len(self.TT) (numer of cores) and row size will change for each dimension.
    :param int ncols: If int then the column size will be the same in all dimensions, if list then len(ncols) == len(self.TT) (numer of cores) and column size will change for each dimension.
    :param float eps: [default == 1e-8] precision with which to approximate the input tensor

    """

    base = None
    basemat = None
    L = None
    __nrows = [] # Real sizes of the tensor matrices
    __ncols = [] # Real sizes of the tensor matrices
    
    def __init__(self,A,base,nrows,ncols,eps=1e-8,is_sparse=False):
        
        self.base = base
        self.basemat = base**2
        
        if isinstance(nrows,int) and isinstance(ncols,int):
            nrows = [nrows]
            ncols = [ncols]

        if len(nrows) != len(ncols): raise NameError("TensorToolbox.QTTmat.__init__: len(nrows)!=len(ncols)")

        self.__nrows = nrows
        self.__ncols = ncols

        if isinstance(A,np.ndarray):
            
            for i,sizedim in enumerate(A.shape):
                if sizedim != self.__nrows[i] * self.__ncols[i]:
                    raise NameError("TensorToolbox.QTTmat.__init__: Array dimension not consistent with nrows and ncols")
                if np.remainder(np.log(sizedim)/np.log(self.basemat),1.0) > np.spacing(1):
                    raise NameError("TensorToolbox.QTTmat.__init__: base is not a valid base of A.size")
            
            self.L = int( np.log(A.size)/np.log(self.basemat) )
            
            # Prepare interleaved idxs (wtf!!!)
            Ls = [ int( np.log(self.__nrows[i]*self.__ncols[i])/np.log(self.basemat) ) for i in range(self.ndims()) ]
            idxs = []
            for j in range(self.ndims()):
                offset = np.sum(2 * Ls[:j],dtype=int)
                for i in range(Ls[j]):
                    idxs.append(offset + i)
                    idxs.append(offset + Ls[j]+i)

            # Fold, re-order and reshape
            A = np.reshape(A,[self.base for i in range(2*self.L)])
            A = np.transpose(A,axes=idxs)
            A = np.reshape(A,[self.basemat for i in range(self.L)])
            
            TTmat.__init__(self,A,nrows=self.base,ncols=self.base,eps=eps)

        elif isinstance(A,list):
            
            TTmat.__init__(self,A,nrows=self.base,ncols=self.base)
            
            # Check that unfolded nrows,ncols are consistent with the dimension of A
            if np.prod(self.shape()) != np.prod(self.__nrows)*np.prod(self.__ncols):
                self.init = False
                raise NameError("TensorToolbox.QTTmat.__init__: unfolded nrows,ncols not consistent with shape of A")
            for nrow,ncol in zip(self.__nrows,self.__ncols):
                if np.remainder(np.log(nrow*ncol)/np.log(self.basemat),1.0) > np.spacing(1):
                    self.init = False
                    raise NameError("TensorToolbox.QTTmat.__init__: base is not a valid base for the selected nrows,ncols")
            
            self.L = len(self.shape()) 
        
        self.init = True
    
    def ndims(self):
        """ Return the number of dimensions of the tensor space
        """
        return len(self.__nrows)

    def get_fullnrows(self):
        """ Returns the number of rows of the unfolded matrices 
        """
        return self.__nrows

    def get_fullncols(self):
        """ Returns the number of cols of the unfolded matrices
        """
        return self.__ncols

    def get_nrows(self):
        """ Returns the number of rows of the folded matrices
        """
        return self.nrows

    def get_ncols(self):
        """ Returns the number of cols of the folded matrices
        """
        return self.nrows
    
    def copy(self):
        newTT = []
        for TTi in self.TT: newTT.append(TTi.copy())
        return QTTmat(newTT,self.base,nrows=list(self.get_fullnrows()),ncols=list(self.get_fullncols()))
    
    def __getitem__(self,idxs):
        """ Get item function
        :param tuple,int idxs: ((i_1,..,i_d),(j_1,..,j_d)) with respect to the unfolded mode sizes

        :returns: item at that position
        """
        if not self.init: raise NameError("TensorToolbox.QTTmat.__getitem__: QTT not initialized correctly")
        
        # Check for out of bounds
        if any(map(operator.ge,idxs[0],self.get_fullnrows())) or any(map(operator.ge,idxs[1],self.get_fullncols())):
            raise NameError("TensorToolbox.QTTmat.__getitem__: Index out of bounds")
        
        # Compute the index of the folding representation from the unfolded index
        return TTmat.__getitem__(self,
                                 ( idxfold( self.get_nrows(), idxunfold(self.get_fullnrows(), idxs[0])),
                                   idxfold( self.get_ncols(), idxunfold(self.get_fullncols(), idxs[1]))) )

    def kron(self,A):
        if not self.init: raise NameError("TensorToolbox.QTTmat.kron: TT not initialized correctly")
        # Additional tests wrt the extend function of TTvec
        if not isinstance(A,QTTmat): raise NameError("TensorToolbox.QTTmat.kron: A is not of QTTmat type")
        if not A.init: raise NameError("TensorToolbox.QTTmat.kron: input tensor is not initialized correctly")
        if self.base != A.base: raise NameError("TensorToolbox.QTTmat.kron: kron product for QTT vectors is allowed only for the same bases")
        
        self.TT.extend(A.TT)
        self.__nrows.extend(A.get_fullnrows())
        self.__ncols.extend(A.get_fullncols())
        self.nrows.extend(A.get_nrows())
        self.ncols.extend(A.get_ncols())
        self.L = len(self.shape())
            
            
