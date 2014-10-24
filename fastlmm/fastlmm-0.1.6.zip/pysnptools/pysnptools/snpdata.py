import numpy as SP
import subprocess, sys, os.path
from itertools import *
import pandas as pd
import logging
from snpreader import SnpReader
from pysnptools.pysnptools.standardizer.unit import Unit
from pysnptools.pysnptools.standardizer.identity import Identity

class SnpData(SnpReader):

    def __init__(self, parent, val):
        '''
        '''
        self._parent = parent
        assert type(val) == SP.ndarray, "expect SnpData's val to be a ndarray"
        self.val = val
        self._std_string = ""

    def __repr__(self):
        s = "SnpData({0}{1})".format(self._parent,self._std_string)
        return s

    def copyinputs(self, copier):
        self._parent.copyinputs(copier)

    @property
    def iid(self):
        return self._parent.iid

    @property
    def sid(self):
        return self._parent.sid

    @property
    def pos(self):
        return self._parent.pos

    def read(self, order='F', dtype=SP.float64, force_python_only=False, view_ok=False):
        if view_ok:  #!!!cmk04072014 regression test
            return self
        else:
            return SnpReader.read(self, order, dtype, force_python_only, view_ok)


    def _read(self, iid_index_or_none, sid_index_or_none, order, dtype, force_python_only):
        val, shares_memory = SnpReader._apply_sparray_or_slice_to_val(self.val, iid_index_or_none, sid_index_or_none, order, dtype, force_python_only)
        if shares_memory:
            val = val.copy(order='K')
        return val

    def standardize(self, standardizer=Unit(), blocksize=None, force_python_only=False):
        self.val = standardizer.standardize(self.val, blocksize=blocksize, force_python_only=force_python_only)
        self._std_string += ",{0}".format(standardizer)
        return self

    def kernel(self, standardizer, blocksize=None, allowlowrank=False):
        if (blocksize is None or self.sid_count <= blocksize) and type(standardizer) is Identity:
            K = self.val.dot(self.val.T)
            return K
        else:
            K = SnpReader.kernel(self, standardizer, blocksize=blocksize, allowlowrank=allowlowrank)
            return K

