#!/usr/bin/env python

from io import open
import os
import sys

from setuptools import setup, find_packages

readme = open('README.rst', encoding='utf-8').read()

setup(name='geoffrey-snakefood',
      version='0.0.1',
      description='Python Dependency Graphs',
      long_description=readme,
      author='Roberto Abdelkader Martínez Pérez',
      author_email='robertomartinezp@gmail.com',
      url='https://github.com/nilp0inter/geoffrey-snakefood',
      include_package_data=True,
      packages=find_packages(),
      namespace_package=['geoffreyplugins'],
)
