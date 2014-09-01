#!/usr/bin/env python

from distutils.core import setup
import json

with open('package.json', 'r') as f:
    version = json.load(f)['version']

setup(name='simworker',
      version=version,
      description='Distributed simulation',
      author='Stanley Gu',
      author_email='stanleygu@gmail.com',
      url='https://github.com/stanleygu/docker-sim-engine-cylinder.git',
      packages=['cylinder']
      )
