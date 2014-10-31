import os

def __bootstrap__():
   global __bootstrap__, __loader__, __file__
   import sys, pkg_resources, imp
   __file__ = pkg_resources.resource_filename(__name__,'api.so')
   __loader__ = None; del __bootstrap__, __loader__
#   imp.load_dynamic(__name__,__file__)
   imp.load_dynamic('capdRedHom',__file__)

__bootstrap__()

from .cubical_complex import *
from .simplicial_complex import *
from .algorithms import *
import persistence
from libcapdapiRedHom_py import Logger
from .version import __version__
