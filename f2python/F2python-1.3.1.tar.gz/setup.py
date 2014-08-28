#!/usr/bin/env python

from distutils.core import setup

with open('README.txt') as readmefile:
	long_description = readmefile.read()
	
setup(name="F2python",
      version="1.3.1",
      description="The F2 DBMS written in Python. Needs ZODB and ZEO to run.",
      author="Thibault Estier",
      author_email="thibault.estier@unil.ch",
      packages=['F2'],
      long_description=long_description
     )
