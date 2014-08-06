#!/usr/bin/env python

from setuptools import setup, find_packages

import pants_utils

setup(
    name='pants-utils',
    version=pants_utils.VERSION,
    packages= find_packages()
)
