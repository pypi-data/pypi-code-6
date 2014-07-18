#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
  name='Pylares',
  packages = find_packages(),
  version='0.0.1',
  description='Helper to use and teach python in Latin American schools.',
  author="Mariano D'Agostino",
  author_email="dagostinom [at] gmail",
  url="https://pypi.python.org/pypi/Pylares",
  download_url='https://github.com/pylares/pylares',
  classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: Spanish",
  ]
)
