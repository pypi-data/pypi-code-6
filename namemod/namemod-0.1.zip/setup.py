'''
Created on 8/06/2014

@author: Ronaldo Webb
'''

from distutils.core import setup
import py2exe

with open('README.txt') as file:
    long_description = file.read()

setup(name='namemod',
      version='0.1',
      author='Ronaldo Webb',
      long_description=long_description,
      packages=['', 'nm.actions', 'nm.args', 'nm.exceptions', 'nm.processors'],
      console=['namemod.py'])