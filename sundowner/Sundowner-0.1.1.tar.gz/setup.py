#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Sundowner',
    version='0.1.1',
    long_description=__doc__,
    packages=['sundowner'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.10',
        'ephem>=3.7',
        'itsdangerous>=0.24',
        'Jinja2>=2.7.2',
        'MarkupSafe>=0.23',
        'Werkzeug>=0.9.4',
        'python-dateutil>=2.2'
    ]
)
