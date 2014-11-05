__version__ = "$Rev: 3318 $"
import pkg_resources
try:
    version = pkg_resources.require(dev)[0].version
except:
    version = __version__


import sif2uniprot
from sif2uniprot import *

