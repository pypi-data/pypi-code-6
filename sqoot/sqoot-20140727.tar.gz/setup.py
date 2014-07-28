#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2014 Rajat Agarwal

from setuptools import setup, find_packages

import sqoot

setup(
    name='sqoot',
    version='20140727',
    author='Rajat Agarwal',
    author_email='rajatagarwal@alumni.purdue.edu',
    url='https://github.com/ragarwal6397',
    description='Sqoot wrapper library',
    long_description=open('./README.txt', 'r').read(),
    download_url='https://github.com/ragarwal6397/sqoot/tarball/master',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: MIT License',
        ],
    packages=find_packages(),
    install_requires=[
        'requests>=2.1',
    ],
    license='MIT License',
    keywords='sqoot api',
    include_package_data=True,
    zip_safe=True,
)
