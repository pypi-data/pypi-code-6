#!/usr/bin/env python

import os.path
import distutils.core

info = {}
execfile(os.path.join(os.path.split(__file__)[0], 'vectortile', 'version.py'), info)
del info['__builtins__']

with open('README.md') as f:
    doc = f.read()

distutils.core.setup(
    name='vectortile',
    description=doc,
    long_description=doc,
    packages=['vectortile', 'vectortile.tests'],
    install_requires=["python-geohash==0.8.4"],
    extras_require = {'test':  ["docopt==0.6.2", "nose==1.3.1", "unittest2==0.5.1"]},
    
    version = info['__version__'],
    author = info['__author__'],
    author_email = info['__author_email__'],
    url= info['__source__'],
    license= info ['__license__']
)
