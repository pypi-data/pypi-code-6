#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from setuptools import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
long_description = readme
doclink = '''
Documentation
-------------

The full documentation is at http://workbench.rtfd.org. '''
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='workbench_cli',
    version='0.1.8',
    description='Command Line Interface for Workbench',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='The Workbench Team',
    author_email='support@supercowpowers.com',
    url='http://github.com/SuperCowPowers/workbench',
    packages=['workbench', 'workbench.clients'],
    package_dir={'workbench': 'workbench'},
    include_package_data=True,
    scripts=['workbench/clients/workbench'],
    install_requires=['colorama', 'ipython', 'pytest', 'zerorpc'],
    license='MIT',
    zip_safe=False,
    keywords='workbench security python',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
