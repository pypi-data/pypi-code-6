#!/usr/bin/env python

from distutils.core import setup

setup(name='benchy',
      version='1.0.1',
      description='simple line by line benchmarking',
      author='Michael Giba',
      author_email='michaelgiba@gmail.com',
      url='michaelgiba.com',
      packages=['benchy'],
      install_requires=['dill'],
      setup_requires=["dill"],
    )
