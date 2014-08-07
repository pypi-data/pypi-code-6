r"""
.. moduleauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""

import numpy as np
from ..data.statelist import StateList

class BasicReader( object ):
    r"""
    I am the basic reader class
    
    Notes
    -----
    I am not the class you're looking for!
    Unless you want to write a new reader class; in that case, feel free to use me :)
    
    """
    def __init__( self, files, skiprows=0, stride=1, maxlength=None, verbose=False ):
        r"""
        Initializes the standard reader class
        
        Parameters
        ----------
        files : list
            contains the names of trajectory files for import
        skiprows : int (optional)
            skip the leading lines
        stride : int (optional)
            use only every <stride> line
        maxlength : int (optional)
            limit the maximal number of samples to use
        verbose : boolean (optional)
            be loud and noisy
        """
        self.files = files
        self.skiprows = skiprows
        self.stride = stride
        self.maxlength = maxlength
        self.verbose = verbose
        self.n_files = len( self.files )
        self.traj_length = np.zeros( shape=(self.n_files,), dtype=np.int32 )
        self.data = []
    def read_trajectories( self ):
        r"""
        Read all the given files' content
        """
        for i in xrange( self.n_files ):
            content = np.loadtxt( self.files[i], skiprows=self.skiprows )
            if ( 1<self.stride ) and ( content.shape[0]>self.stride ):
                content = content[::self.stride,:]
            if ( None!=self.maxlength ) and ( content.shape[0]>self.maxlength ):
                content = content[:self.maxlength,:]
            self.data.append( np.zeros( shape=content.shape, dtype=np.float64 ) )
            self.data[-1][:,:] = content[:,:]
            self.traj_length[i] = self.data[-1].shape[0]
            if self.verbose:
                print "Read %d frames from file %s" % ( self.traj_length[i], self.files[i] )
    def get_states( self ):
        r"""
        Extract the state indices from the imported data
        
        Returns
        -------
        states : pyfeat.data.StateList object
            contains lists of markov & thermodynamic states
        """
        states = StateList( self.n_files, self.data, self.traj_length, verbose=self.verbose )
        return states
