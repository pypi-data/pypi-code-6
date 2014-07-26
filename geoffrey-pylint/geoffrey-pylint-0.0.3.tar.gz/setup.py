#!/usr/bin/env python

from io import open
import os
import sys

from setuptools import setup, find_packages

readme = open('README.rst', encoding='utf-8').read()

setup(name='geoffrey-pylint',
      version='0.0.3',
      description='python code static checker',
      long_description=readme,
      author='Roberto Abdelkader Martínez Pérez',
      author_email='robertomartinezp@gmail.com',
      url='https://github.com/GeoffreyCI/geoffrey-pylint',
      include_package_data=True,
      packages=find_packages(),
      namespace_package=['geoffreyplugins'],
)
