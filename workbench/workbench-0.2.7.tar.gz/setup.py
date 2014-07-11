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
    name='workbench',
    version='0.2.7',
    description='A medium-data framework for security research and development teams.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Brian Wylie',
    author_email='briford@supercowpowers.com',
    url='https://github.com/SuperCowPowers/workbench',
    packages=['workbench','workbench.clients', 'workbench.server',
              'workbench.server.bro', 'workbench.workers',
              'workbench.workers.rekall_adapter'],
    package_dir={'workbench': 'workbench'},
    include_package_data=True,
    scripts = ['workbench/workbench'],
    tests_require=['tox'],
    install_requires=['elasticsearch', 'urllib3', 'filemagic', 'pefile', 'py2neo',
                      'pymongo', 'requests', 'cython', 'ssdeep==2.9-0.3', 'watchdog',
                      'yara', 'funcsigs', 'zerorpc', 'distorm3>=0', 'rekall==1.0rc11',
                      'pytest', 'coverage', 'pytest-cov', 'tox'],
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
