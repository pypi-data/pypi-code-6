r"""
.. moduleauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>, Antonia Mey <antonia.mey@fu-berlin.de>

"""

import numpy as np
from .basicreader import BasicReader
from ..data.data import Data

class Reader( BasicReader ):
    r"""
    I am a reader
    """
    def __init__( self, files, kT_file =None, wham_file = None, kT_target=None, skiprows=0, stride=1, maxlength=None, verbose=False ):
        r"""
        Initializes the standard reader class
        
        Parameters
        ----------
        files : list
            contains the names of trajectory files for import
        kT_file : string (optinal)
            import kT values from file
        wham_file : string (optional)
            import reduced markov state bias energies from file
        kT_target : float (optional)
            target temperature ( uses lowest kT if not given)
        skiprows : int (optional)
            skip the leading lines
        stride : int (optional)
            use only every <stride> line
        maxlength : int (optional)
            limit the maximal number of samples to use
        verbose : boolean (optional)
            be loud and noisy
        """
        super( Reader, self ).__init__( files, skiprows=skiprows, stride=stride, maxlength=maxlength, verbose=verbose )
        if kT_file!=None:
            self.kT = np.loadtxt(kT_file)
            if kT_target==None:
                self.kT_target = self.kT.min()
            else:
                self.kT_target = kT_target
        else:
            self.kT=None
        if wham_file!=None:
            self.wham = np.loadtxt(wham_file)
        else:
            self.wham=None
    def build_data_object( self ):
        self.read_trajectories()
        states = self.get_states()
        u_ijt=None
        uu_jt=None
        if self.kT!=None and states.replica_width==3:
            u_ijt=self.build_tensor_kT(states)
        elif states.replica_width==3+states.n_therm_states:
            [u_ijt,uu_jt]=self.build_tensor(states)
        elif self.wham==None:
            raise RuntimeError("Trajectory format not appropriate, missing data")
        [ eu_ijt , eshift_jt ] = self.build_shift_and_tensor( u_ijt )
        return Data( states, u_ijt=u_ijt, wham=self.wham, uu_jt=uu_jt, eu_ijt=eu_ijt, eshift_jt=eshift_jt )
    def build_tensor_kT(self, states):
        u_ijt = np.zeros( shape=(states.n_therm_states,states.n_therm_states,states.max_therm_samples), dtype=np.float64 )
        t = np.zeros( shape=(states.n_therm_states,), dtype=np.int32 )
        for f in xrange( states.n_replicas ):
            for l in xrange( states.replica_length[f] ):
                j = states.therm_state[f,l]
                for i in xrange( states.n_therm_states ):
                    u_ijt[i,j,t[j]] = self.data[f][l,2] *  self.kT[j] / self.kT[i] -  self.data[f][l,2]*self.kT[j]/self.kT_target
                t[j] += 1
        return u_ijt
    def build_tensor(self, states):
        t = np.zeros( shape=(states.n_therm_states,), dtype=np.int32 )
        u_ijt = np.zeros( shape=(states.n_therm_states,states.n_therm_states,states.max_therm_samples), dtype=np.float64 )
        uu_jt = np.zeros( shape=(states.n_therm_states,states.max_therm_samples), dtype=np.float64 )
        for f in xrange( states.n_replicas ):
            for l in xrange( states.replica_length[f] ):
                j = states.therm_state[f,l]
                for i in xrange( states.n_therm_states ):
                    #u_ijt[i,j,t[j]] = self.data[f][l,2] + self.data[f][l,3+i]
                    u_ijt[i,j,t[j]] = self.data[f][l,3+i]
                uu_jt[j,t[j]] = self.data[f][l,2]
                t[j] += 1
        return [ u_ijt , uu_jt ]
    def build_shift_and_tensor( self, u_ijt ):
        shift_jt = np.amin( u_ijt, axis=0 )
        eu_ijt = np.exp( shift_jt[np.newaxis,:,:] - u_ijt )
        return [ eu_ijt , np.exp( shift_jt ) ]
        
        

