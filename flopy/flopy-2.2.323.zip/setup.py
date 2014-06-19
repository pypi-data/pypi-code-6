import sys
from distutils.core import setup

# To use:
#	   python setup.py bdist --format=wininst

from flopy import __version__, __name__, __author__

setup(name=__name__,
      description='FloPy is a Python package to create, run, and post-process MODFLOW-based models.',
      long_description='FloPy includes support for MODFLOW-2000, MODFLOW-2005, and MODFLOW-NWT. Other supported MODFLOW-based models include MT3D and SEAWAT.',
      author=__author__,
      author_email='mark.bakker@tudelft.nl, vincent.post@flinders.edu.au, langevin@usgs.gov, jdhughes@usgs.gov, jwhite@usgs.gov, frances.alain@gmail.com',
      url='https://code.google.com/p/flopy/',
      license='New BSD',
      platforms='Windows, Mac OS-X',
      packages=['flopy','flopy.modflow','flopy.mt3dms','flopy.seawat','flopy.utils'],
      # use this version ID if .svn data cannot be found
      version=__version__ )
