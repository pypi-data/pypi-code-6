r"""

=====================
WHAM estimator module
=====================

.. moduleauthor:: Antonia Mey <antonia.mey@fu-berlin.de>, Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""

import numpy as np
from ...exception.exception import NotConvergedWarning

__all__ = [ 'WHAM' ]

class WHAM( object ):
    r"""
    I run the WHAM estimator
    """
    def __init__( self, data, free_energies=None ):
        r"""
        Initialize the WHAM object
        
        Parameters
        ----------
        data : pyfeat.data.Data object
            contains the u_ijt tensor and additional informations
        free_energies : np.array( shape=(number_of_thermodynamic_states,) )
            contains an initial guess for the free energy estimation
        
        """
        self.data = data
        nm = self.data.states.n_markov_states
        nt = self.data.states.n_therm_states
        nr = self.data.states.n_replicas
        if None == free_energies:
            self.free_energies = np.ones( shape=(nt,), dtype=np.float64 )*0.0001
        else:
            self.free_energies = free_energies
        self.f = np.exp( self.free_energies )
        self.probabilities = np.zeros( shape=(nm,), dtype=np.float64 )
        self.gradient_norm = None
        self.a = np.exp( -self.data.wham.transpose() )
        self.c = np.zeros( shape=(nt,nm), dtype=np.int32 )
        for r in xrange( nr ):
            for l in xrange( self.data.states.replica_length[r] ):
                self.c[ self.data.states.therm_state[r,l] , self.data.states.markov_state[r,l] ] += 1
    def scf_iteration( self, maxiter=100, ftol=1.0e-5, verbose=False ):
        r"""function of the self consisten wham equations iteration
        
        Parameters
        ----------
        maxiter : int (optional)
            number of allowed iterations Default = 100
        ftol : double (optional)
            tolerance for the convergence
        verbose : boolean (optional)
            be loud and noisy if verbose=True
        
        """
        if verbose:
            print "# %6s %10s" % ( "[Step]", "[Increment]" )
        if np.all( self.probabilities == 0.0 ):
            self.probabilities[:] = self._p_step()
        for i in xrange( maxiter ):
            f_new = self._f_step()
            nonzero = self.f.nonzero()
            a = np.log( f_new[nonzero] / self.f[nonzero] )
            b = np.log( self.f[nonzero] )
            nonzero = b.nonzero()
            self.ferr = np.max( np.abs( a[nonzero] / b[nonzero] ) )
            self.f[:] = f_new[:]
            self.probabilities = self._p_step()
            if verbose:
                print "  %6d %10.3e" % ( i+1, self.ferr )
            if self.ferr <ftol:
                break
        if self.ferr>=ftol:
            raise NotConvergedWarning
        self.free_energies = np.log( self.f )
        self.probabilities /= self.probabilities.sum()
    def _f_step( self ):
        return 1.0 / np.dot( self.a, self.probabilities ) + np.log( self.probabilities.sum() )
    def _p_step( self ):
        return self.c.sum( axis=0 ) / np.dot( self.c.sum( axis=1 ) * self.f , self.a )
