#!/usr/bin/env python
from setuptools import setup
import os
import sys

py_entry = 'wpy%s = pythonwpy.__main__:main'
endings = ('', sys.version[:1], sys.version[:3])
entry_points_scripts = []
for e in endings:
    entry_points_scripts.append(py_entry % e)

setup(
    name='pythonwpy',
    version='0.4.0',
    description='python -c, with tab completion and shorthand',
    license='MIT',
    url='https://github.com/Russell91/pythonwpy',
    long_description='https://github.com/Russell91/pythonwpy',
    packages = ['pythonwpy'],
    entry_points = {
        'console_scripts': entry_points_scripts
    },
)
