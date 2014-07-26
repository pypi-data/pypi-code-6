#!/usr/bin/env python

from io import open
import os
import sys

from setuptools import setup, find_packages

readme = open('README.rst', encoding='utf-8').read()

setup(name='geoffrey-jshint',
      version='0.0.1',
      description='JSHint is a community-driven tool to detect errors and potential problems in JavaScript code',
      long_description=readme,
      author='Miguel Reguero Bejar',
      author_email='mreguerob0@gmail.com',
      url='https://github.com/GeoffreyCI/geoffrey-jshint',
      include_package_data=True,
      packages=find_packages(),
      namespace_package=['geoffreyplugins'],
)
