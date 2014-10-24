#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = [str(r.req) for r in parse_requirements('requirements.txt')]
test_reqs = [str(r.req) for r in parse_requirements('test-requirements.txt')]

setup(name='hyperspace',
      version='0.0.1',
      py_modules = ['hyperspace'],
      description='General-purpose REST/hypermedia client.',
      author='Ross Fenning',
      author_email='ross.fenning@gmail.com',
      url='http://rossfenning.co.uk/',
      packages=['hyperspace'],
      install_requires=install_reqs,
      tests_require=test_reqs
     )
