#!/usr/bin/env python
from setuptools import setup

import os.path as op
CURRENT_DIR = op.dirname(__file__)

version = '0.1.2'

requirements = open(op.join(CURRENT_DIR, 'requirements.txt')).read()

setup(name='log_watcher',
    packages=['log_watcher'],

    version=version,
    include_package_data=True,
    zip_safe=False,
    install_requires=[line for line in requirements.splitlines() if line and not line.startswith("--")],
    entry_points='''
        [console_scripts]
        log_watcher=log_watcher.cli:main
    ''',
)
