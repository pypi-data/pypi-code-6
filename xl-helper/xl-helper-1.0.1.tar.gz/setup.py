#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='xl-helper',
      version='1.0.1',
      description='XL Deploy helper',
      long_description='This tool helps with installation and upgrade of XL Deploy and plugins',
      author='Mike Kotsur',
      author_email='mkotsur@xebialabs.com',
      url='http://xebialabs.com/',
      packages=list(find_packages()),
      install_requires=['jenkinsapi', 'argparse'],
      scripts=['bin/xl-helper']
)
