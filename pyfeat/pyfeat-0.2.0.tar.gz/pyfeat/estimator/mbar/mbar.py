r"""

=====================
MBAR estimator module
=====================

.. moduleauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""

import numpy as np
from .ext import mbar_eq, mbar_binning, mbar_binning_state
from ...exception.exception import NotConvergedWarning

__all__ = [ 'MBAR' ]

class MBAR( object ):
    r"""
    I run the MBAR estimator
    """
    def __init__( self, data, free_energies=None ):
        r"""
        Initialize the MBAR object
        
        Parameters
        ----------
        data : pyfeat.data.Data object
            contains the u_ijt tensor and additional informations
        free_energies : np.array( shape=(number_of_thermodynamic_states,) )
            contains an initial guess for the free energy estimation
        
        """
        self.data = data
        self.gradient_norm = None
        self.ferr = None
        if None == free_energies:
            self.free_energies = np.ones( shape=(self.data.states.n_therm_states,) )*0.001
        else:
            self.free_energies = free_energies
        self.probabilities = np.zeros( shape=(self.data.states.n_markov_states,), dtype=np.float64 )
    def scf_iteration( self, maxiter=100, ftol=1.0e-5, verbose=False ):
        r"""
        Estimate the free energies via fixed point iteration
        
        Parameters
        ----------
        maxiter : integer
            maximum number of scf steps
        ftol : floating point number
            relative error convergence criterion
        verbose : boolean
            write convergence progress to stdout
        
        """
        emf_new = np.exp( -self.free_energies )
        emf = np.empty_like( emf_new )
        if verbose:
            print "# %6s %10s" % ( "[Step]", "[Increment]" )
        for i in xrange( maxiter ):
            emf[:] = emf_new[:]
            if self.data.equal_samples():
                mbar_eq( emf, self.data.eu_ijt, emf_new )
            else:
                mbar_eq( emf, self.data.eu_ijt, emf_new, self.data.states.therm_sample )
            emf_new /= emf_new.max()
            nonzero = emf.nonzero()
            a = -np.log( emf_new[nonzero] / emf[nonzero] )
            b = -np.log( emf[nonzero] )
            nonzero = b.nonzero()
            self.ferr = np.max( np.abs( a[nonzero] / b[nonzero] ) )
            if verbose:
                print "  %6d %10.3e" % ( i+1, self.ferr )
            if self.ferr < ftol:
                break
        if self.ferr>=ftol:
            raise NotConvergedWarning()
        self.free_energies = -np.log( emf_new )
    def get_probabilities( self, state=None ):
        r"""
        Estimate the markov states' probabilities
        
        Parameters
        ----------
        state : integer (optional)
            computes the markov states' probabilities for a given thermodynamic state
        
        """
        if None == state:
            if self.data.equal_samples():
                mbar_binning(
                        np.exp(-self.free_energies),
                        self.data.eu_ijt,
                        self.data.eshift_jt,
                        self.data.states.markov_sequence,
                        self.probabilities
                    )
            else:
                mbar_binning(
                        np.exp(-self.free_energies),
                        self.data.eu_ijt,
                        self.data.eshift_jt,
                        self.data.states.markov_sequence,
                        self.probabilities,
                        self.data.states.therm_sample
                    )
        else:
            if self.data.equal_samples():
                mbar_binning_state(
                        np.exp(-self.free_energies),
                        self.data.eu_ijt,
                        state,
                        self.data.states.markov_sequence,
                        self.probabilities
                    )
            else:
                mbar_binning_state(
                        np.exp(-self.free_energies),
                        self.data.eu_ijt,
                        state,
                        self.data.states.markov_sequence,
                        self.probabilities,
                        self.data.states.therm_sample
                    )
