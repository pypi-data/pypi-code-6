#!/usr/bin/env python
from setuptools import setup, find_packages

# for having nose collector work correctly.
import multiprocessing

setup(
    name='sparql11',
    version='0.0.1',
    author='Thomas Scharrenbach',
    author_email='thomas@scharrenbach.net',
    packages=['sparql11'],
    url='http://scharrenbach.net',
    license='LICENSE.txt',
    description='SPARQL1.1 protocol compliant endpoint',
    long_description=open('README.txt').read(),
    install_requires=[],
	setup_requires=['rdflib>=4.0',
					'nose>=1.0','mock'],
    test_suite = 'nose.collector',
	scripts=['bin/sparql11-server.py'],
	)
