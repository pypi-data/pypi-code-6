r"""

MBAR
----

.. moduleauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

This is the API function to run the MBAR estimator on the imported data ::

   from pyfeat import run_mbar
   result = run_mbar( data )

"""

import numpy as np
from .mbar import MBAR
from ...data.result import Result
from ...exception.exception import NotConvergedWarning

__all__ = [ 'run_mbar' ]

def run_mbar( data, free_energies=None, maxiter=100, ftol=1.0e-5, verbose=False ):
    r"""
    API function to run MBAR
    
    Parameters
    ----------
    data : pyfeat.data.Data object
        contains the u_ijt tensor and additional informations
    free_energies : np.array( shape=(number_of_thermodynamic_states,) )
        contains an initial guess for the free energy estimation
    maxiter : integer
        maximum number of fixed point interation steps
    ftol : floating point number
        gradient-based convergence criterion
    verbose : boolean
        write convergence progress to stdout
    
    Returns
    -------
    result : pyfeat.data.Result object
        estimated free energies and probabilities
    
    """
    mbar_obj = MBAR( data, free_energies=free_energies )
    try:
        mbar_obj.scf_iteration( maxiter=maxiter, ftol=ftol, verbose=verbose )
    except NotConvergedWarning:
        print "Careful! Self consistent iteration is not converged!"
    mbar_obj.get_probabilities()
    return Result( data.states, mbar_obj.free_energies, mbar_obj.probabilities )
