#!/usr/bin/env python

from distutils.core import setup

setup(name='EnvComparison',
      version='0.1',
      description='Linux Environment Comparison Tool',
      author='Andrew Martin',
      author_email='a.a.d.martin@gmail.com',
      url='https://github.com/adamar/EnvComparison',
      scripts=["compare.py"],
      #install_requires=["paramiko", "tornado"],
      packages=['EnvComparison']
     )
