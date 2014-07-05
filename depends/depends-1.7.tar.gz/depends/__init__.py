'''
Created on Jun 18, 2014

@author: francis
'''

import sys

from Depends import dep, depends, isSatisfied, ndep, satisfy, strict, lazy, \
    verify, flatten, satisfied, unsatisfied, allSatisfied, allReady, \
    ready
from Errors import CircularDependencyError, InvalidDependantName, DependsError

__author__ = 'Francis Horsman'
__version__ = '1.7'
__email__ = 'francis.horsman@gmail.com'
__doc__ = 'A dependency graph creator and checker'

del sys
