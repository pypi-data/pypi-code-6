#!/usr/env python
# -*- coding: utf-8 -*-
"""
python-limelight
~~~~~~~~~~~~~~~~

An object-oriented API wrapper for `Lime Light CRM`_

.. _Lime Light CRM: https://www.limelightcrm.com
"""

from setuptools import setup

setup(name='python-limelight',
      version='1',
      description='A pythonic Lime Light API wrapper',
      long_description=open('README.rst', 'r').read(),
      url='https://github.com/heropunch/python-limelight',
      license='MIT',
      author='Carlos Killpack',
      author_email='carlos.killpack@rocketmail.com',
      packages=('limelight', 'limelight.transaction', 'limelight.membership'),
      classifiers=('Environment :: Web Environment',
                   'Topic :: Internet',
                   'Topic :: Office/Business',
                   'Topic :: Office/Business :: Financial',
                   'Topic :: Office/Business :: Financial :: Accounting',
                   'Topic :: Office/Business :: Financial :: Investment',
                   'Topic :: Office/Business :: Financial :: Point-Of-Sale',
                   'License :: OSI Approved',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: Implementation :: PyPy', ),
      install_requires=('validate-email-address>=1',
                        'requests',
                        'ipaddress',
                        'voluptuous',
                        'pycountry',
                        'six', ))
