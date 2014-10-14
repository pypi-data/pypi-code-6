#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from os.path import abspath, dirname, join

from sys import path

# get setup directory abspath
_path = dirname(abspath(__file__))

# import utils
path.append(_path)
import b3j0f.utils as package

# get long description
with open(join(_path, 'README')) as f:
    desc = f.read()

setup(
    name=package.__name__,
    version=package.__version__,
    packages=find_packages(exclude=['test.*', '*.test.*']),
    package_dir={'': '.'},
    author="b3j0f",
    author_email="jlabejof@yahoo.fr",
    description="b3j0f utils",
    long_description=desc,
    include_package_data=True,
    url='https://github.com/mrbozzo/utils/',
    license='MIT License',
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    test_suite='b3j0f'
)
