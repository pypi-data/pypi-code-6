#!/usr/bin/env python3
#
#  Copyright (c) 2014, Corey Goldberg (cgoldberg@gmail.com)
#
#  license: GNU GPLv3
#
#  This file is part of: subunit-details
#  https://github.com/cgoldberg/subunit-details
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; version 3 of the
#  License.


"""
setup/install script for subunitdetails

"""

from setuptools import setup


with open('README.rst') as f:
    LONG_DESCRIPTION = '\n' + f.read() + '\n'

setup(
    name='subunitdetails',
    version='0.0.3',
    author='Corey Goldberg',
    author_email='cgoldberg _at_ gmail.com',
    description='SubUnit Details Parser - Test Detail attachment extractor.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/cgoldberg/subunitdetails',
    download_url='http://pypi.python.org/pypi/subunitdetails',
    keywords='subunit parser unittest testtools testing'.split(),
    license='GNU GPLv3',
    packages=['subunitdetails'],
    install_requires=['python-subunit', 'testtools'],
    entry_points={
        'console_scripts':['subunitdetails=subunitdetails.subunitdetails:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Office/Business :: Financial :: Investment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Testing',
    ]
)
