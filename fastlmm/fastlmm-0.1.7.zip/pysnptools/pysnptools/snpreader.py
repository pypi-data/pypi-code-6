import numpy as SP
import subprocess, sys
import os.path
from itertools import *
import pandas as pd
import logging
import time

class SnpReader(object):
    '''
    A SnpReader instance is
        - an instance of a primitive SnpReader that can read genotype data from disk, such as
               primitive = Bed('../../tests/datasets/all_chr.maf0.001.N300')
        - an instance of SnpData (details below) which holds its own copy of the genotype data in memory
        - a subset of any SnpReader instance, 
                 such as subset1 = primitive[:,::-1]
                 and     subset2 = subset1[[3,4],::2]

    SnpReaders print nicely:
        print primitive #prints: Bed('../../tests/datasets/all_chr.maf0.001.N300')
        print subset2   #prints: Bed('../../tests/datasets/all_chr.maf0.001.N300')[:,::-1][[3,4],::2]

    A SnpData instance is created by applying the .read(order='F',...) method to any SnpReader instance. For example,
                 primitive = Bed('../../tests/datasets/all_chr.maf0.001.N300')
                 snpdata1 = primitive.read()
                 print snpdata1 #prints SnpData(Bed('../../tests/datasets/all_chr.maf0.001.N300'))
                 snpdata2 = primitive[:,::-1][[3,4],::2].read(order='C')
                 snpdata3 = snpdata2.read(order='F')
                 print snp_data3 #prints SnpData(SnpData(Bed('../../tests/datasets/all_chr.maf0.001.N300')[:,::-1][[3,4],::2]))

    All SnpReader instances these properties:
       - iid: list of iids #!!!cmk05192014 LATER are these specially numpy arrays?
       - iid_count: number of iids
       - sid: list of sids
       - sid_count: number of sids
       - pos: list of position information
    and these methods:
       - read(order='F'): creates an in memory SnpData with a copy of the genotype data
       - iid_to_index(iid_list): take a list of iids and returns a list of index numbers
       - sid_to_index(sid_list): take a list of sids and returns a list of index numbers
       - kernel(kernel_maker=Correlation()): returns a SnpKernel
       - [,]  : creates a SnpReader that will read a subset of the genotype data

    A SnpData instance supports all the SnpReader properites and methods and adds:
        - val : a NumPy array of the genotype data.
        - std(standardizer=Unit()) : Does in-place standardization. For convincence, returns "self", the SnpData instance.

    Generally, when a SnpReader instance is constructed no data is read or accessed. Thus, construction
    of SnpReader instances is very inexpensive.
           For example, no data is read, accessed, or processed by these statements:
                     primitive=Bed('../../tests/datasets/all_chr.maf0.001.N300')
                     subset5=primitive[[3,4],:]
   
   The first time that iid or sid info is requested, the iid and sid info (but not the genotype info)
   is read and stored.  Because, iid and sid info is relatively small, this is relatively inexpensive.
           For example, the ".sid_count" access causes the iid and sid values to be read from the file and stored.
                    primitive=Bed('../../tests/datasets/all_chr.maf0.001.N300')
                    print primitive.sid_count
           If we now request: 
                    print primitive.iid_count
           nothing need be read again because the iid and sid information was already
           stored in the instance.

    Genotype data is read only with the ".read(order='F')" method. 
    To the degree possible, only the iids and sids previously specified by subsetting
    are read from the file.

    '''

    def copyinputs(self, copier):
        raise NotImplementedError

    @property
    def iid(self):
        raise NotImplementedError

    @property
    def sid(self):
        raise NotImplementedError

    @property
    def pos(self):
        raise NotImplementedError

    def _read(self, iid_index_or_none, sid_index_or_none, order, dtype, force_python_only):
        raise NotImplementedError

    @property
    def iid_count(self):
        return len(self.iid)

    @property
    def sid_count(self):
        return len(self.sid)

    def read(self, order='F', dtype=SP.float64, force_python_only=False, view_ok=False):
        val = self._read(None, None, order, dtype, force_python_only)
        from snpdata import SnpData
        ret = SnpData(self, val)
        return ret

    def iid_to_index(self, list):
        if not hasattr(self, "_iid_to_index"):
            self._iid_to_index = {}
            for index, item in enumerate(self.iid):
                key = (item[0],item[1])
                if self._iid_to_index.has_key(key) : raise Exception("Expect iid to appear in data only once. ({0})".format(key))
                self._iid_to_index[key] = index
        index = SP.fromiter((self._iid_to_index[(item1[0],item1[1])] for item1 in list),SP.int)
        return index

    def sid_to_index(self, list):
        if not hasattr(self, "_sid_to_index"):
            self._sid_to_index = {}
            for index, item in enumerate(self.sid):
                if self._sid_to_index.has_key(item) : raise Exception("Expect snp to appear in data only once. ({0})".format(item))
                self._sid_to_index[item] = index
        index = SP.fromiter((self._sid_to_index[item1] for item1 in list),SP.int)
        return index

    def __getitem__(self, iid_indexer_and_snp_indexer):
        from _subset import _Subset
        iid_indexer, snp_indexer = iid_indexer_and_snp_indexer
        return _Subset(self, iid_indexer, snp_indexer)


    def kernel(self, standardizer, blocksize=10000, allowlowrank=False):

        #print "entering kernel with {0},{1},{2}".format(self, standardizer, blocksize)
        """build kernel by loading blocks of SNPs
        """
        t0 = time.time()
        K = SP.zeros([self.iid_count,self.iid_count])

        logging.info("reading {0} SNPs in blocks of {1} and adding up kernels (for {2} individuals)".format(self.sid_count, blocksize, self.iid_count))

        ct = 0
        ts = time.time()

        if (not allowlowrank) and self.sid_count < self.iid_count: raise Exception("need to adjust code to handle low rank")

        from pysnptools.pysnptools.standardizer.identity import Identity
        for start in xrange(0, self.sid_count, blocksize):
            ct += blocksize
            snpdata = self[:,start:start+blocksize].read().standardize(standardizer)
            K += snpdata.kernel(Identity())
            if ct % blocksize==0:
                logging.info("read %s SNPs in %.2f seconds" % (ct, time.time()-ts))


        # normalize kernel
        #K = K/sp.sqrt(self.sid_count)

        #K = K + 1e-5*sp.eye(N,N)     
        t1 = time.time()
        logging.info("%.2f seconds elapsed" % (t1-t0))

        #print "leaving kernel with {0},{1},{2}".format(self, standardizer, blocksize)
        return K


    @staticmethod
    def _is_all_slice(index_or_none):
        if index_or_none is None:
            return True
        return  isinstance(index_or_none,slice) and index_or_none == slice(None)

    @staticmethod
    def _make_sparray_or_slice(indexer):
        if indexer is None:
            return slice(None)

        if isinstance(indexer,SP.ndarray):
            if indexer.dtype == bool:
                return SP.arange(len(indexer))[indexer]
            else:
                return indexer

        if isinstance(indexer, slice):
            return indexer

        if isinstance(indexer, int):
            return SP.array([indexer])

        return SP.array(indexer)

    @staticmethod
    def _make_sparray_from_sparray_or_slice(count, indexer):
        if isinstance(indexer,slice):
            return apply(SP.arange, indexer.indices(count))
        return indexer


    @staticmethod
    def _array_properties_are_ok(val, order, dtype):
        if val.dtype != dtype:
            return False
        if order is 'F':
            return val.flags['F_CONTIGUOUS']
        elif order is 'C':
            return val.flags['C_CONTIGUOUS']

        return True

    @staticmethod
    def _apply_sparray_or_slice_to_val(val, iid_indexer_or_none, sid_indexer_or_none, order, dtype, force_python_only):
        if SnpReader._is_all_slice(iid_indexer_or_none) and SnpReader._is_all_slice(sid_indexer_or_none) and order is None and dtype is None and force_python_only is None:
            return val, True
        else:
            iid_indexer = SnpReader._make_sparray_or_slice(iid_indexer_or_none)
            sid_indexer = SnpReader._make_sparray_or_slice(sid_indexer_or_none)
            if SnpReader._is_all_slice(iid_indexer) or SnpReader._is_all_slice(sid_indexer):
                sub_val = val[iid_indexer, sid_indexer]
            else:
                #See http://stackoverflow.com/questions/21349133/numpy-array-integer-indexing-in-more-than-one-dimension
                sub_val = val[iid_indexer.reshape(-1,1), sid_indexer]
        assert len(sub_val.shape)==2, "Expect result of subsetting to be 2 dimensional"

        if not SnpReader._array_properties_are_ok(sub_val, order, dtype):
            if order is None:
                order = "K"
            if dtype is None:
                dtype = sub_val.dtype
            sub_val = sub_val.astype(dtype, order, copy=True)

        shares_memory =  SP.may_share_memory(val, sub_val)
        assert(SnpReader._array_properties_are_ok(sub_val, order, dtype))
        return sub_val, shares_memory


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import doctest
    doctest.testmod()
