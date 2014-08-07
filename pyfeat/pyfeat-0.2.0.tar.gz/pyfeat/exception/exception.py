r"""
.. moduleauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>, Antonia Mey <antonia.mey@fu-berlin.de>


"""

import numpy as np

class NotConvergedWarning(Exception):
    r"""
    Exception class for non-convergence of estimators
    """
    pass 


class NotConnectedSetError( Exception ):
    r"""
    Exception class for not connected sets
    """
    pass


class MissingThermodynamicStatesError( Exception ):
    r"""
    Exception class for not connected sets
    """
    pass
