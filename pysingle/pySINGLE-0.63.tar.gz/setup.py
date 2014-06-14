#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
import numpy

setup(name='pySINGLE', 
    packages = ['pySINGLE'],
    version='0.63', 
    description = 'Python implementation of SINGLE algorithm',
    author = 'Ricardo Pio Monti',
    author_email = 'ricardo.monti08@gmail.com',
    url = 'https://github.com/piomonti/pySINGLE',
    download_url = 'https://github.com/piomonti/pySINGLE/tarball/0.1',
    ext_modules = [Extension("Z_shooting", ["Z_shooting.pyx"],)],
    include_dirs=[numpy.get_include(),'.', ],
    #py_modules=['pySINGLE']
    )
