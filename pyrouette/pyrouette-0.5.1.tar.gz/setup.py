'''
Created on May 5, 2009

@author: stober
'''

from setuptools import setup, find_packages
from setuptools.extension import Extension
import numpy
import os

np_lib = os.path.dirname(numpy.__file__)
np_inc = [os.path.join(np_lib, 'core/include')]

# doesn't work yet
ext_modules = [Extension("cmac.fast", sources = ["pyrouette/cmac/fast.c"], include_dirs=np_inc),
               Extension("pca.fast", ["pyrouette/pca/fast_pca.c"], include_dirs=np_inc)]

DESCRIPTION = """
Pyrouette is a collection of Python modules that provide a straightforward, lightweight framework for
experimenting with artificial intelligence algorithms. The goal is to make algorithm implementations readable and
easily modifiable, and to provide a simple set of pre-configured experiments. """

print find_packages(exclude=('bin','external'))

setup(name='pyrouette',
      version='0.5.1',
      description='A pythonic machine learning library',
      author='Jeremy Stober',
      author_email='stober@gmail.com',
      packages= find_packages(exclude=('bin',)),
      license="BSD",
      ext_package='pyrouette',
      ext_modules=ext_modules,
      url="http://pyrouette.org",
      keywords="machine learning algorithms cmac",
      long_description=DESCRIPTION,
      classifiers=["Programming Language :: Python",
                   "License :: OSI Approved :: BSD License",
                   "Development Status :: 4 - Beta"]
      )
