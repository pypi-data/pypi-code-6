import os
from setuptools import setup
from pbr import util
import pyul 

os.environ['PBR_VERSION'] = pyul.__version__
setup(**util.cfg_to_args())
