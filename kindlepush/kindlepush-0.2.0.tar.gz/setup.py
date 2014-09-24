#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from kindlepush import kindlepush

setup(
    name='kindlepush',
    version=kindlepush.__version__,
    description='Automatically send your doc to your kindle without clicking the deliver button for 3G device',
    url='https://github.com/lord63/kindledxpush',
    author='lord63',
    author_email='lord63.j@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='kindle push automatically 3G',
    packages=['kindlepush'],
    install_requires=['requests', 'beautifulsoup4', 'terminal'],
    entry_points={
        'console_scripts': [
            'kindlepush=kindlepush.kindlepush:main',
        ],
    },
)
