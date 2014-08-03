#!/usr/bin/env python
# encoding: utf-8
'''
Created on 3 Aug 2014

@author: Liam Deacon

@contact: liam.deacon@diamond.ac.uk

@copyright: 2014 Liam Deacon

@license: MIT License

'''
try:
    from setuptools import find_packages
except ImportError:
    from distutils.core import find_packages

from distutils.core import setup
import os.path

setup(name='igor2txt',
      version='0.1',
      description='Extract ASCII waves from Igor *.pxp, *.pxt & *.ibw files',
      author='Liam Deacon',
      author_email='liam.deacon@diamond.ac.uk',
      url='http://www.python.org/igor2txt/',
      license='MIT License',
      packages=find_packages(),
      long_description=open(os.path.join('.','README.rst')
            ).read() if os.path.exists(os.path.join('.','README.rst')) else None,
      classifiers=[
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: Chemistry',
            'Topic :: Scientific/Engineering :: Physics',
            ],
      keywords='phaseshifts atomic scattering muffin-tin diffraction',
      install_requires=['numpy', 'igor'],
      scripts=['igor2txt.py']
)
