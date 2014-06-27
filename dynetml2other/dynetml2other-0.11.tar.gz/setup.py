#!/usr/bin/env python

__author__ = 'plandweh'


from distutils.core import setup

setup(name='dynetml2other',
      version='0.11',
      description='DyNetML parsing and manipulation',
      long_description=open('README.rst').read(),
      author='Peter Landwehr',
      author_email='plandweh@cs.cmu.edu',
      license='BSD',
      url='http://pmlandwehr.github.io/dynetml2other/',
      requires=['lxml'],  # Neither igraph nor networkx are required to build the package.
      packages=['dynetml2other'],
      package_dir={'dynetml2other': 'dynetml2other'}
     )