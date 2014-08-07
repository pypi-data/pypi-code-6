r"""

WHAM
====

.. moduleauthor:: Antonia Mey <antonia.mey@fu-berlin.de>, Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

This is the API function to run the WHAM estimator on the imported data ::

   from pyfeat import run_wham
   result = run_wham( data )

"""

from .wham import WHAM
from ...data.result import Result
from ...exception.exception import NotConvergedWarning

__all__ = [ 'run_wham' ]

def run_wham( data, free_energies=None, maxiter=100, ftol=1.0e-5, verbose=False ):
    r"""
    API function to run WHAM
    
    Parameters
    ----------
    data : pyfeat.data.Data object
        contains the u_ijt tensor and additional informations
    free_energies : np.array( shape=(number_of_thermodynamic_states,) )
        contains an initial guess for the free energy estimation
    maxiter : integer (optional)
        maximum number of fixed point interation steps
    ftol : floating point number (optional)
        gradient-based convergence criterion
    verbose : boolean (optional)
        write convergence progress to stdout
    
    Returns
    -------
    result : pyfeat.data.Result object
        estimated free energies and probabilities
    
    """
    wham_obj = WHAM( data, free_energies=free_energies )
    try:
        wham_obj.scf_iteration( maxiter=maxiter, ftol=ftol, verbose=verbose )
    except NotConvergedWarning:
        print "Careful! Self consistent iteration is not converged!"
    return Result( data.states, wham_obj.free_energies, wham_obj.probabilities )
