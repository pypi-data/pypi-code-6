#!/usr/bin/env python
from setuptools import setup, find_packages

import os.path as op
CURRENT_DIR = op.dirname(__file__)

version = '0.1.0'

requirements = open(op.join(CURRENT_DIR, 'requirements.txt')).read()

setup(name='log_watcher',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[line for line in requirements.splitlines() if line and not line.startswith("--")]
)
