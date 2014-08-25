#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'src'))

from quant import __version__

basePath = os.path.abspath(os.path.dirname(sys.argv[0]))
scripts = [ 
    os.path.join('bin', 'quant-makeconfig'),
    os.path.join('bin', 'quant-admin'),
    os.path.join('bin', 'quant-test'),
    os.path.join('bin', 'quantvirtualenvhandlers.py'),
]

long_description = open('README').read() + open('INSTALL').read()

setup(
    name='quant',
    version=__version__,

    package_dir={'': 'src'},
    packages=find_packages('src'),
    scripts=scripts,
    # just use auto-include and specify special items in MANIFEST.in
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'domainmodel==0.16',
        'python-dateutil',
        'quantdsl',
        'scipy',
        'numpy',
        'mock', # For testing...
    ],
    author='Appropriate Software Foundation',
    author_email='quant-support@appropriatesoftware.net',
    license='AGPL',
    url='http://appropriatesoftware.net/quant',
    description='Enterprise architecture for quantitative analysis in finance.',
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
   ],
)
