# -*- coding: utf-8 -*-
# from distutils.core import setup
import os
import sys
from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

version = '1.0.0'

setup(
    name='bootd',
    version=version,
    author=u'ShinZ Natkid',
    author_email='shinznatkid@gmail.com',
    packages=find_packages(),
    url='http://github.com/shinznatkid/bootd',
    license='MIT',
    include_package_data=True,
    description='Wizard startproject from django base template.',
    long_description=open('README.md').read(),
    zip_safe=False,
    scripts=['bootd/bin/bootd-admin.py'],
    install_requires=[
        "django>=1.6.5",
        "django-picker>=0.1.6",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ]
)
