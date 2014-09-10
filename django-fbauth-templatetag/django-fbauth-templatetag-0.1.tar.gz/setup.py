#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from io import open
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-fbauth-templatetag',
    version='0.1',
    packages=find_packages(exclude='demo'),
    license='BSD',
    url='https://github.com/hellhound/django-fbauth',
    author='Jean-Pierre Chauvel',
    author_email='jchauvel@gmail',
    description='Django app that comes with a simple template tag to place a ' \
        'Facebook log-in button in your template',
    long_description=open(os.path.join(
        os.path.dirname(__file__), 'README.rst'), encoding='utf-8').read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django >= 1.6',
    ]
)
