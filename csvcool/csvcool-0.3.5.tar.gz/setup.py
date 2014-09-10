#!/usr/bin/env python
#-*-coding:utf-8-*-

# "THE WISKEY-WARE LICENSE":
# <jbc.develop@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a WISKEY in return Juan BC


#===============================================================================
# DOCS
#===============================================================================

"""Setup for csvcool (http://bitbucket.org/leliel12/csvcool)"""


#===============================================================================
# IMPORTS
#===============================================================================

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

import csvcool


#===============================================================================
# SETUP
#===============================================================================

setup(name=csvcool.__name__,
      version=csvcool.__version__,
      description=csvcool.__doc__.splitlines()[0],
      long_description=csvcool.__doc__,
      author=csvcool.__author__,
      author_email=csvcool.__email__,
      url=csvcool.__url__,
      license="GPL3",
      keywords="csv",
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Topic :: Utilities",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2",
                   ],
      py_modules = ['csvcool', 'ez_setup'],
      test_suite = "test",
)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == '__main__':
    print(__doc__)
