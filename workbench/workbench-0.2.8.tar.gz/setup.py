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
    version='0.2.8',
    description='A medium-data framework for security research and development teams.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='The Workbench Team',
    author_email='support@supercowpowers.com',
    url='http://github.com/SuperCowPowers/workbench',
    packages=['workbench', 'workbench.clients', 'workbench.server',
              'workbench.server.bro', 'workbench.workers',
              'workbench.workers.rekall_adapter'],
    package_dir={'workbench': 'workbench'},
    include_package_data=True,
    scripts=['workbench/server/workbench_server', 'workbench/clients/workbench'],
    tests_require=['tox'],
    install_requires=['coverage', 'cython', 'distorm3>=0', 'elasticsearch',
                      'funcsigs', 'filemagic', 'pefile', 'py2neo', 'pymongo',
                      'pytest>=2.5', 'pytest-cov', 'rekall==1.0rc11', 'requests',
                      'ssdeep==2.9-0.3', 'tabulate', 'tox', 'urllib3', 'watchdog',
                      'yara', 'zerorpc'],
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
