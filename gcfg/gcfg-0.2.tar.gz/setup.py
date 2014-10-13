from __future__ import print_function

import gcfg

try: from distutils.core import setup
except ImportError: from setuptools import setup

setup(
      name='gcfg',
      version=gcfg.__version__,
      license="MIT",
      description='convert *.ini to python Model for easy access',

      author='codeskyblue',
      author_email='codeskyblue@gmail.com',
      url='http://github.com/codeskyblue/gcfg',

      py_modules=["gcfg"],
      install_requires=[],
      )
