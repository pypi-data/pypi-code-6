#!/usr/bin/env python
from setuptools import setup, find_packages

# for having nose collector work correctly.
import multiprocessing

setup(
    name='lrdgdal',
    version=open('version.txt').read(),
    author='Thomas Scharrenbach',
    author_email='thomas@scharrenbach.net',
    packages=find_packages(),
    include_package_data=True,
    url='http://scharrenbach.net',
    license='Apache License v2',
    description='Linked Raster Data for gdal for python',
    long_description=open('README.txt').read(),
    install_requires=['lxml>=3.3,',
                      'rdflib>=4.0',
                      'gdal>=1.10',
                      'numpy>=1.8'],
    setup_requires=['nose>=1.0', 'mock'],
    test_suite='nose.collector')
