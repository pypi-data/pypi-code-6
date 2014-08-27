#!/usr/bin/env python

from distutils.core import setup
import json

with open('../package.json') as f:
    version = json.load(f)['version']

setup(name='simclient',
            version=version,
            description='Tools for IPython Notebook used with Tellurium',
            author='Stanley Gu',
            author_email='stanleygu@gmail.com',
            url='https://github.com/stanleygu/sim-engine-scheduler',
            packages=['.']
            )
