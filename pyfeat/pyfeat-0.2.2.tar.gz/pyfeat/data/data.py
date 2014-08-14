r"""

==============
Data container
==============

.. moduleauthor:: Antonia Mey <antonia.mey@fu-berlin.de>, Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

"""

import numpy as np

class Data( object ):
    r"""
    Container for the u[i,j,t] tensor
    """
    def __init__( self, states, u_ijt=None, uu_jt=None, wham=None, eu_ijt=None, eshift_jt=None ):
        r"""
        Initialize the u[i,j,t] tensor
        
        Parameters
        ----------
        states : pyfeat.data.StateList object
            includes state sequences and counts
        u_ijt : np.ndarray( shape=(i,j,t) )
            legacy
        uu_jt : np.ndarray( shape=(j,t) ) or None
            legacy
        wham : np.ndarray( shape=(n_markov_states,n_therm_states) )
            reduced bias energies of the markov states in all thermodynamic potentials
        eu_ijt : np.ndarray( shape=(n_therm_states,n_therm_states,max_therm_samples) )
            $eu_{ijt}=\exp(-u^{(i)}(x_t^{(j)}))$
        eshift_jt : np.ndarray( shape=(n_therm_states,max_therm_samples) )
            shift values for numerical stability ($u^{(i)}(x_t^{(j)}) \geq 0\,\forall i$)
        """
        # store reduced energy tensors and/or wham matrix
        self.u_ijt = u_ijt # legacy
        self.uu_jt = uu_jt # legacy
        self.wham = wham
        self.eu_ijt = eu_ijt
        self.eshift_jt = eshift_jt
        # store StateList object
        self.states = states
        # misc
        self.equal_samples_flag = None
        # sanity checks
        if ( None == self.u_ijt ) and ( None == self.wham ):
            raise RuntimeError( "Missing data: either u_ijt or wham must be supplied" )
    def equal_samples( self ):
        r"""
        Checks if all thermodynamic states have equal number of samples
        
        Returns
        -------
        equal_samples : boolean
            True if samples numbers are equal
        """
        if None == self.equal_samples_flag:
            self.equal_samples_flag = np.all( self.states.therm_sample == self.states.max_therm_samples )
        return self.equal_samples_flag


