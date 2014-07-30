#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='sleekdigda',
    version='0.2.0',
    description='XEP-Digda - SleekXMPP plugin',
    long_description=open('README.md').read(),
    author='Optiflows R&D',
    author_email='rand@optiflows.com',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=[
        'setuptools_git==1.0',
    ],
    install_requires=[
        'sleekxmpp>=1.3.0,<1.4.0',
    ],
)
