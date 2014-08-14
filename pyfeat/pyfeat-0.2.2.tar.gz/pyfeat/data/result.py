r"""

=====================
Result data container
=====================

.. moduleauthor:: Antonia Mey <antonia.mey@fu-berlin.de>, Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""

import numpy as np

class Result( object ):
    r"""
    Results data container class
    """
    def __init__( self, states, fi_therm, pi_markov ):
        r"""
        Initializes the results container

        Parameters
        ----------
        states : pyfeat.data.StateList object
            just a reference
        fi_therm ; np.ndarray( shape=(n_therm_states,) )
            thermodynamic free energies
        pi_markov : np.ndarray( shape=(n_markov_states,) )
            markov probabilities
        """
        self.states = states
        self.fi_markov = np.zeros( shape=(self.states.n_markov_states,), dtype=np.float64 )
        self.pi_markov = np.zeros( shape=(self.states.n_markov_states,), dtype=np.float64 )
        self.fi_therm = np.zeros( shape=(self.states.n_therm_states,), dtype=np.float64 )
        self.fi_therm[:] = fi_therm[:]
        self.pi_markov[:] = pi_markov[:] / pi_markov.sum()
        self.fi_markov[:] = -np.log( self.pi_markov )
    def print_markov( self ):
        r"""
        Print out the probabilities and reduced free energies of all markov states
        """
        print "# %21s %21s %21s" % ( '[markov state]' , '[probability]' , '[reduced free energy]' )
        for i in xrange( self.fi_markov.shape[0] ):
            print "  %20d  %20.14f  %20.12f" % ( i , self.pi_markov[i], self.fi_markov[i] )
