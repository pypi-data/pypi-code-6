from __future__ import print_function

import os
import sys
import imp

from setuptools import setup, find_packages

setup(
    name='layers',
    version='0.1.0',
    author='Alex Rudakov',
    author_email='ribozz+layers@gmail.com',
    maintainer='Alex Rudakov',
    maintainer_email='ribozz+layers@gmail.com',
    url='https://github.com/ribozz/layers',
    description='Layered source layouts for software development projects',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    install_requires=[],

    entry_points={
        'console_scripts': [
            'layers = layers:main'
        ],
    }
)
