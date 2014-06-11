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

__all__ = ['QTTvec','QTTzerosvec']

import operator
import numpy as np
from TensorToolbox.core import TTvec
from TensorToolbox.core import idxfold, idxunfold

class QTTvec(TTvec):
    """ Constructor of multidimensional tensor in Quantics Tensor Train format
        
    :param ndarray,TT A: Available input formats are full tensor in numpy.ndarray, Tensor Train structure (list of cores)
    :param int base: folding base for QTT representation
    :param list,int shape: if QTTvec is constructed from a list of cores, shape must be provided to describe the original shape of the vector
    :param float eps: [default == 1e-8] precision with which to approximate the input tensor

    """

    base = None
    L = None
    __shape = None
    
    def __init__(self,A,base,shape=None,eps=1e-10):
        
        # Initialize the tensor with the input tensor in TT ([][]numpy.ndarray), tensor(numpy.ndarray)
        # if isinstance(A,Candecomp):
        #     self.TT = A.to_TT()

        self.base = base

        if isinstance(A,np.ndarray):

            if shape != None: raise NameError("TensorToolbox.QTTvec.__init__: shape argument is unnecessary for ndarray input")
            
            for sizedim in A.shape:
                if np.remainder(np.log(sizedim)/np.log(base),1.0) > np.spacing(1):
                    raise NameError("TensorToolbox.QTTvec.__init__: base is not a valid base of A.size")
            
            self.L = int( np.log(A.size)/np.log(self.base) )
            self.__shape = A.shape

            # Folding matrix
            A = np.reshape(A,[self.base for i in range(self.L)])
            
            TTvec.__init__(self,A,eps)
        elif isinstance(A,list):
            if shape == None: raise NameError("TensorToolbox.QTTvec.__init__: shape argument is mandatory for TT input")
            for sizedim in shape:
                if np.remainder(np.log(sizedim)/np.log(base),1.0) > np.spacing(1):
                    raise NameError("TensorToolbox.QTTvec.__init__: base is not a valid base of shape")

            TTvec.__init__(self,A)

            # Check that the size is consistent with base
            size = np.prod(self.shape())
            if np.remainder(np.log(size)/np.log(base),1.0) > np.spacing(1):
                self.init = False
                raise NameError("TensorToolbox.QTTvec.__init__: base is not a valid base of A.size()")

            self.L = int( np.log(size)/np.log(self.base) )
            self.__shape = shape
            
        else:
            raise NameError("TensorToolbox.TTvec.__init__: Input type not allowed")
        
        self.init = True

    def copy(self):
        newTT = []
        for TTi in self.TT: newTT.append(TTi.copy())
        return QTTvec(newTT,self.base,list(self.__shape))

    def fullshape(self):
        """ Return the shape of the folded tensor
        """
        return self.__shape

    def __getitem__(self,idxs):
        """ Get item function: indexes are entered in with respect to the unfolded mode sizes.
        """
        if not self.init: raise NameError("TensorToolbox.QTTvec.__getitem__: QTT not initialized correctly")
        
        # Check whether index out of bounds
        if any(map(operator.ge,idxs,self.qttshape())):
            raise NameError("TensorToolbox.QTTvec.__getitem__: Index out of bounds")

        # Compute the index of the folding representation from the unfolded representation
        return TTvec.__getitem__(self,idxfold(self.shape(),idxunfold(self.fullshape(),idxs)))
        
    def kron(self,A):
        if not self.init: raise NameError("TensorToolbox.QTTvec.kron: TT not initialized correctly")
        # Additional tests wrt the extend function of TTvec
        if not isinstance(A,QTTvec): raise NameError("TensorToolbox.QTTvec.kron: A is not of QTTvec type")
        if not A.init: raise NameError("TensorToolbox.QTTvec.kron: input tensor is not initialized correctly")
        if self.base != A.base: raise NameError("TensorToolbox.QTTvec.kron: kron product for QTT vectors is allowed only for the same bases")
        
        self.TT.extend(A.TT)
        self.__shape.extend(A.fullshape())
        self.L = int( np.log(self.shape())/np.log(self.base) )
        
        
##########################################################
# Constructors of frequently used tensor vectors
##########################################################

def QTTzerosvec(d,N,base):
    """ Returns the rank-1 multidimensional vector of zeros in Quantics Tensor Train format
    
    Args:
       d (int): number of dimensions
       N (int or list): If int then uniform sizes are used for all the dimensions, if list of int then len(N) == d and each dimension will use different size
       base (int): QTT base
    
    Returns:
       QTTvec The rank-1 multidim vector of zeros in Tensor Train format
    """
    from TensorToolbox.core import Candecomp
    from TensorToolbox.core import zerosvec

    if isinstance(N,int):
        N = [N for i in range(d)]
    
    for sizedim in N:
        if np.remainder(np.log(sizedim)/np.log(base),1.0) > np.spacing(1):
            raise NameError("TensorToolbox.QTTvec.QTTzerosvec: base is not a valid base of N")
    
    L = int( np.log(np.prod(N))/np.log(base) )

    tt = zerosvec(L,[base for i in range(L)])

    return QTTvec(tt.TT, base, shape=N)
