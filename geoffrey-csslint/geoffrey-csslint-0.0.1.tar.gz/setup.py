#!/usr/bin/env python

from io import open
import os
import sys

from setuptools import setup, find_packages

readme = open('README.rst', encoding='utf-8').read()

setup(name='geoffrey-csslint',
      version='0.0.1',
      description='CSSLint is a tool to help point out problems with your CSS code.',
      long_description=readme,
      author='Miguel Reguero Bejar',
      author_email='mreguerob0@gmail.com',
      url='https://github.com/GeoffreyCI/geoffrey-csslint',
      include_package_data=True,
      packages=find_packages(),
      namespace_package=['geoffreyplugins'],
)
