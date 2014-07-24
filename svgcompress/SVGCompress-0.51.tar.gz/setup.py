from setuptools import setup

## The following is an alternative to install_requires for
## libraries that seem to have issues when installing from pip
try:
    import numpy
except ImportError:
    raise ImportError("Please install numpy")

try:
    import shapely
except ImportError:
    raise ImportError('Please install Shapely')

setup(
      name         = 'SVGCompress',
      packages     = ['SVGCompress'],
      version      = '0.51',
      description  = 'Compress svg graphics',
      author       = 'Gen Del Raye',
      author_email = 'gdelraye@hawaii.edu',
      url          = '',
      download_url = '',
      keywords     = ['figure', 'vector', 'svg', 'compression'],
      install_requires = ['svg.path', 'rdp', 'lxml', 'scour'],
      package_data = {'SVGCompress': ['test/*.svg']},
      classifiers  = [
                      "Intended Audience :: Science/Research",
                      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                      "Natural Language :: English",
                      "Operating System :: OS Independent",
                      "Programming Language :: Python",
                      "Topic :: Scientific/Engineering",
                      "Topic :: Scientific/Engineering :: Visualization"],
      )