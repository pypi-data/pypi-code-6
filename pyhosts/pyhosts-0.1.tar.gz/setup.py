#!/usr/bin/env python

from setuptools import setup

import pyhosts

setup(name="pyhosts",
      version=0.1,
      description="Pythonic way to manage hosts file.",
      author="Igor Milovanovic",
      author_email="igor@tnkng.com",
      url="http://github.com/pletisan/pyhosts/",
      test_suite='nose.collector',
      packages=['pyhosts'],
      )
