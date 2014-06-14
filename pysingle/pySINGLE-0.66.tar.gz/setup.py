#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

#extension = [Extension("Z_shooting", ["Z_shooting.c"],),]

setup(name='pySINGLE', 
    packages = ['pySINGLE'],
    version='0.66', 
    description = 'Python implementation of SINGLE algorithm',
    author = 'Ricardo Pio Monti',
    author_email = 'ricardo.monti08@gmail.com',
    url = 'https://github.com/piomonti/pySINGLE',
    download_url = 'https://github.com/piomonti/pySINGLE/tarball/0.1',
    
    #ext_modules = cythonize("pySINGLE/Z_shooting.pyx"),
    #include_dirs=[numpy.get_include(),'.', ],
    #py_modules=['pySINGLE']
    )
