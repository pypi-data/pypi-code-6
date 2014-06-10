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

__all__ = ['TensorWrapper']

import operator
import itertools
import random
import shutil
import os.path
import numpy as np
import numpy.linalg as npla
import scipy.linalg as scla
import pickle as pkl
import marshal, types
import warnings
try:
    import mpi_map
    MPI_SUPPORT = True
except ImportError:
    MPI_SUPPORT = False

from TensorToolbox.core import idxunfold, idxfold, object_store

class TensorWrapper():
    """ A tensor wrapper is a data structure W that given a multi-dimensional scalar function f(X,params), and a set of coordinates {{x1}_i1,{x2}_i2,..,{xd}_id} indexed by the multi index {i1,..,id}, let you access f(x1_i1,..,xd_id) by W[i1,..,id]. The function evaluations are performed "as needed" and stored for future accesses.

    :param f: multi-dimensional scalar function of type f(x,params), x being a list.
    :param list X: list of arrays with coordinates for each dimension
    :param tuple params: parameters to be passed to function f
    :param string twtype: 'array' values are stored whenever computed, 'view' values are never stored and function f is always called
    :param dict data: initialization data of the Tensor Wrapper (already computed entries)
    :param int range_shape: specify the shape of the objects in the tensor wrapper
    :param bool empty: Creates an instance without initializing it. All the content can be initialized using the ``setstate()`` function.
    :param int maxprocs: Number of processors to be used in the function evaluation (MPI)

    """
    f = None
    f_code = None               # Marshal string of the function f
    X = None
    params = None
    dtype = object
    shape = None
    ndim = None
    size = None
    twtype = None
    data = None
    store_file = ""
    store_object = None
    __maxprocs = None             # Number of processors to be used (MPI)

    serialize_list = ['X', 'dtype', 'params', 'shape', 'ndim', 'size', 'twtype', 'data','store_file', 'f_code']
    
    def __init__(self, f, X, params=None, twtype='array', data=None, dtype=object,
                 store_file = "", store_object = None,
                 empty=False,
                 maxprocs=None,
                 marshal_f=True):
        if not empty: 
            self.set_f(f,marshal_f)
            self.params = params
            self.X = X
            self.shape = self.get_shape()
            self.ndim = len(self.shape)
            self.size = self.get_size()
            self.twtype = twtype
            self.dtype = dtype
            self.store_file = store_file
            self.store_object = store_object
            self.set_maxprocs(maxprocs)
            if self.twtype == 'array':
                if data == None:
                    self.data = {} # Dictionary in python behave as a hash-table
                else:
                    self.data = data
            elif self.twtype != 'view':
                raise ValueError("Tensor Wrapper type not existend. Use 'array' or 'view'")
    
    def __getstate__(self):
        return dict( [ (tag, getattr( self, tag )) for tag in self.serialize_list ] )

    def __setstate__(self,state,f = None, store_object = None):
        for tag in state.keys():
            setattr(self, tag, state[tag])
        # Reset additional parameters
        if f == None: self.reset_f_marshal()
        else: self.set_f(f)
        self.store_object = store_object

    def getstate(self):
        return self.__getstate__();
    
    def setstate(self,state,f = None, store_object = None):
        return self.__setstate__(state, f, store_object)

    def copy(self):
        return TensorWrapper(self.f, self.X, params=self.params, twtype=self.twtype, data=self.data.copy())

    def get_size(self):
        return reduce(operator.mul, self.get_shape())
    
    def get_ndim(self):
        """ Always returns the number of dimensions of the original tensor
        """
        return len(self.get_shape())

    def get_shape(self):
        """ Always returns the shape of the of the original tensor
        """
        dim = [ len(coord) for coord in self.X ]
        return tuple(dim)

    def get_fill_level(self):
        if self.twtype == 'view': return 0
        else: return len(self.data.keys())

    def reshape(self,newshape):
        if np.prod(self.get_shape()) != np.prod(newshape):
            raise ValueError("total size of new array must be unchanged")
        self.shape = newshape
        self.ndim = len(newshape)
    
    def get_fill_idxs(self):
        return self.data.keys()
    
    def get_data(self):
        return self.data
    
    def get_X(self):
        return self.X

    def get_params(self):
        return self.params
    
    def set_f(self,f,marshal_f=True):
        self.f = f
        if self.f != None and marshal_f:
            self.f_code = marshal.dumps(self.f.func_code)
    
    def reset_f_marshal(self):
        if self.f_code != None:
            code = marshal.loads(self.f_code)
            self.f = types.FunctionType(code, globals(), "f")
        else:
            warnings.warn("TensorToolbox.TensorWrapper: The tensor wrapper has not function code to un-marshal. The function is undefined. Define it using TensorToolbox.TensorWrapper.set_f", RuntimeWarning)
    
    def set_maxprocs(self,maxprocs):
        self.__maxprocs = maxprocs
        try:
            import mpi_map
            MPI_SUPPORT = True
        except ImportError:
            MPI_SUPPORT = False
        
        if self.__maxprocs != None and not MPI_SUPPORT:
            warnings.warn("TensorToolbox.TensorWrapper: MPI is not supported on this machine. The program will run without it.", RuntimeWarning)
        
    def set_store_object(self, store_object):
        self.store_object = store_object
    
    def store(self):
        if self.store_file != "":
            if self.store_object != None:
                if self.store_object.to_be_stored(): object_store(self.store_file, self.store_object)
            else:
                object_store(self.store_file, self)

    def __getitem__(self,idxs_in):
        # Transform the tuple to a list for convinience
        idxs_in = list(idxs_in)
        
        # Slice notation can be used. Remember: slice(start:stop:step)
        if len(idxs_in) != len(self.shape):
            raise IndexError('too many indices')
        
        # Check that all the lists are of the same length
        int_idx = []
        list_idx = []
        slice_idx = []
        slice_IDXs = []
        out_shape = []
        llen = None
        for i,idx in enumerate(idxs_in):
            if isinstance(idx, int):
                int_idx.append(i)
            if isinstance(idx, list) or isinstance(idx,tuple):
                list_idx.append(i)
                idxs_in[i] = list(idx)
                if llen == None:
                    llen = len(idx)
                elif llen != len(idx):
                    raise IndexError('List of indices must have the same length.')
            if isinstance(idx, slice):
                slice_idx.append(i)
                IDXs = range(idx.start if idx.start != None else 0,
                                 idx.stop  if idx.stop  != None else self.shape[i],
                                 idx.step  if idx.step  != None else 1)
                slice_IDXs.append( IDXs )
                out_shape.append(len(IDXs))
        
        if llen == None: llen = 1

        # Expand single indices in idxs_in to llen
        for i in int_idx: idxs_in[i] = [idxs_in[i]] * llen
        
        # Create list of index of the in the lists
        list_idx = []
        list_IDXs = []
        for i,idx in enumerate(idxs_in):
            if isinstance(idx, list):
                list_idx.append(i)
                list_IDXs.append( idx )
        if len(list_idx) == 0: list_IDXs.append( [-1] ) # Ghost element added to make the full slicing work
        unlistIdxs = itertools.izip(*list_IDXs)

        transpose_list_shape = False
        if llen > 1: 
            out_shape.insert(0,llen)
            if len(slice_idx) > 0 and len(list_idx) > 0 and min(list_idx) > max(slice_idx):
                transpose_list_shape = True
        
        # Un-slice sliced idxs
        unslicedIdxs = itertools.product(*slice_IDXs)

        # Final list of indices (iterator)
        lidxs = itertools.product(unlistIdxs, unslicedIdxs)
        
        # Allocate output array
        if len(out_shape) > 0:
            out = np.empty(out_shape, dtype=self.dtype)
            
            # MPI code
            eval_i =[]
            eval_idxs = []
            eval_xx = []
            # End MPI code

            for i,(lidx,sidx) in enumerate(lidxs):
                # Reorder the idxs
                idxs = [None for j in range(len(idxs_in))]
                for j,jj in enumerate(list_idx): idxs[jj] = lidx[j]
                for j,jj in enumerate(slice_idx): idxs[jj] = sidx[j]
                idxs = tuple(idxs)
                
                # Separate field idxs from parameter idxs                
                if self.twtype == 'array':
                    # Check whether the value has already been computed
                    try:
                        out[idxfold(out_shape,i)] = self.data[idxs]
                    except KeyError:
                        # Evaluate function
                        xx = np.array( [self.X[ii][idx] for ii,idx in enumerate(idxs)] )

                        # MPI code
                        eval_i.append(i)
                        eval_idxs.append(idxs)
                        eval_xx.append(xx)
                        # End MPI code

                else:
                    # Evaluate function
                    xx = np.array([self.X[ii][idx] for ii,idx in enumerate(idxs)])
                    out[idxfold(out_shape,i)] = self.f(xx,self.params)
            
            # Evaluate missing values
            if self.__maxprocs == None or not MPI_SUPPORT:
                # Serial evaluation
                for (i,idxs,xx) in zip(eval_i, eval_idxs, eval_xx):
                    self.data[idxs] = self.f(xx,self.params)
                    self.store()
                    out[idxfold(out_shape,i)] = self.data[idxs]
            elif len(eval_xx) > 0:
                # MPI code
                eval_res = mpi_map.mpi_map_code( self.f_code, eval_xx, self.params, self.__maxprocs )
                for (i,idxs,res) in zip(eval_i, eval_idxs, eval_res):
                    self.data[idxs] = res
                    out[idxfold(out_shape,i)] = self.data[idxs]
                self.store()
                # End MPI code
            
            if transpose_list_shape:
                out = np.transpose( out , tuple( range(1,len(out_shape)) + [0] ) )
            
        else:
            idxs = tuple(itertools.chain(*lidxs.next()))
            # Separate field idxs from parameter idxs
            if self.twtype == 'array':
                try:
                    out = self.data[idxs]
                except KeyError:
                    # Evaluate function
                    xx = np.array([self.X[ii][idx] for ii,idx in enumerate(idxs)])
                    self.data[idxs] = self.f(xx,self.params)
                    self.store()
                    out = self.data[idxs]
            else:
                out = self.f(np.array([self.X[ii][idx] for ii,idx in enumerate(idxs)]),self.params)
            return out
        
        return out

