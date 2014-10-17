#!/usr/bin/env python

from setuptools import setup

setup(
    name='tinderpy',   
    version='0.0.1',
    description='Tinder client for python',
    author='Michael Valladolid',
    author_email='mikevalladolid@gmail.com',
    url='https://github.com/codenut/tinderpy',
    license='MIT',
    packages=['tinderpy'],
    install_requires=[
        'requests', 
      ]
  )
