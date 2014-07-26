#!/usr/bin/env python

from io import open
import os
import sys

from setuptools import setup, find_packages

readme = open('README.rst', encoding='utf-8').read()

setup(name='geoffrey-cheesecake',
      version='0.0.1',
      description='rank Python packages based on various empirical "kwalitee" factors',
      long_description=readme,
      author='Miguel Reguero Bejar',
      author_email='mreguerob0@gmail.com',
      url='https://github.com/GeoffreyCI/geoffrey-cheesecake',
      include_package_data=True,
      packages=find_packages(),
      namespace_package=['geoffreyplugins'],
)
