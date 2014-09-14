#coding=utf-8
#----------------------------------------------------------
# File: setup.py    Author(s): Alexandre Blondin Massé
#                              Simon Désaulniers
# Date: 2014-03-10
#----------------------------------------------------------
# Setup script for the polyomino enumeration python script.
#----------------------------------------------------------

import os

import ez_setup
# makes sure the right version of setuptools installed
ez_setup.use_setuptools()

from setuptools import setup, find_packages
from Cython.Distutils import build_ext
from Cython.Build import cythonize

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    # meta-data for setuptools
    name             = 'polyenum',
    version          = '0.1-1',
    author           = 'Alexandre Blondin Massé,'
                       'Simon Désaulniers',
    author_email     = 'alexandre.blondin.masse@gmail.com,'
                       'rostydela@gmail.com',
    maintainer       = 'Simon Désaulniers',
    maintainer_email = 'rostydela@gmail.com',
    description      = 'Set of enumerators of multiple types of polyominoes '
                       '(snake, tree, etc.)',
    long_description = read('README.rst'),
    license          = 'GPLv3',
    keywords         = 'polyominoes enumeration combinatorics mathematics',
    classifiers      = ['Topic :: Scientific/Engineering :: Mathematics'],
    url              = 'https://bitbucket.org/ablondin/polyenum',
    scripts          = ['scripts/polyenum'],
    packages         = ['polyenum'],
    requires         = ['cython'],
    install_requires = ['cython'],

    # building
    setup_requires   = ['cython'],
    cmdclass         = {'build_ext': build_ext},
    ext_modules      = cythonize("polyenum/*.pyx")
)
