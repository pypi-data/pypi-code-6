#!/usr/bin/env python
"""
Camera object and routines for dealing with it
"""

import numpy as np
import random





class Camera(object):
    def __init__(self,cM=None,dC=None,rmse=None):
        if cM is None:
            self.cM = np.zeros((2,3))
        else:
            self.cM=cM
        if dC is None:
            self.dC = np.zeros(5)
        else:
            self.dC=dC
        if rmse is None:
            self.rmse = np.inf
        else:
            self.rmse=rmse

    @property
    def fx(self):
        return self.cM[0,0]
    @property
    def cx(self):
        return self.cM[0,2]
    @property
    def cy(self):
        return self.cM[1,2]
    @property
    def AR(self):
        return self.cM[1,1]/self.cM[0,0]
    @property
    def s(self):
        return self.cM[0,1]
    @property
    def k1(self):
        return self.dC[0,0]
    @property
    def k2(self):
        return self.dC[0,1]
    @property
    def t1(self):
        return self.dC[0,2]
    @property
    def t2(self):
        return self.dC[0,3]
    @property
    def k3(self):
        return self.dC[0,4]

    def __str__(self):
        return "{0.fx},{0.cx},{0.cy},{0.AR},{0.s},{0.k1},{0.k2},{0.t1},{0.t2},{0.k3},{0.rmse}".format(self)

    def _from_vec(cls,vec):
        cM = np.array([[vec[0],vec[4],vec[1]],[0.,vec[0]*vec[3],vec[2]],[0.,0.,1.]],dtype=np.float32)
        dC = np.array([[vec[5],vec[6],vec[7],vec[8],vec[9]]],dtype=np.float32)
        rmse = vec[10]
        return cls(cM,dC,rmse)
    from_vec = classmethod(_from_vec)









        

        
