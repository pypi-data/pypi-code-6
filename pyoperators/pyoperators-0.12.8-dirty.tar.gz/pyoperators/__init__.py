"""
The PyOperators package contains the following modules or packages:

- core : defines the Operator class
- linear : defines standard linear operators
- nonlinear : defines non-linear operators (such as thresholding or rounding)
- iterative : defines iterative algorithms working with operators
- utils : miscellaneous routines
- operators_mpi : MPI operators (even if mpi4py is not present)
- operators_pywt : (optional) loaded if PyWavelets is present.

"""

from .utils import *
from .utils.mpi import MPI
from .core import *
from .fft import *
from .linear import *
from .nonlinear import *
from .operators_mpi import *
from .proxy import *
from . import iterative
from .iterative import pcg
from .rules import rule_manager
from .warnings import PyOperatorsWarning

try:
    from .operators_pywt import *
except(ImportError):
    pass

import types
__all__ = [f for f in dir() if f[0] != '_' and not isinstance(eval(f),
           types.ModuleType)]

del f  #XXX not necessary with Python3
del types

I = IdentityOperator()
O = ZeroOperator()
X = Variable('X')

__version__ = '0.12.8-dirty'
