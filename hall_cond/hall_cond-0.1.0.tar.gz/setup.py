#!/usr/bin/env python
from setuptools import setup

import hall_cond

setup(name="hall_cond",
      version=hall_cond.__version__,
      description="A Lightweight Hall Conductivity Computational Library",
      packages=['hall_cond'],
      license='GPLv3 or later',
      install_requires=[
		  "numpy >= 1.7.1",
		  "matplotlib >= 1.2.1",
],)
