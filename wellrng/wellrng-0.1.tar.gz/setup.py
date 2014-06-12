import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
  name = 'wellrng',
  packages = ['wellrng'], # this must be the same as the name above
  version = '0.1',
  description = 'A replacment for the default random lib using WELL1024a RNG',
  author = 'Raphael Stefanini',
  author_email = 'stef.raphael@gmail.com',
  url = 'https://github.com/rphlo/py-wellrng',
  download_url = 'https://github.com/rphlo/py-wellrng/tarball/0.1',
  keywords = ['random', 'well1024a', 'PRNG', 'RNG'],
  classifiers = [],
)
