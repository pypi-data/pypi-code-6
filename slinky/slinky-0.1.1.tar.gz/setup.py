#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [line.strip() for line in open('requirements.txt')
                              .readlines()]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='slinky',
    version='0.1.1',
    description='Quick command to create signed links on S3',
    long_description=readme + '\n\n' + history,
    author='Ben Hughes',
    author_email='bwghughes@gmail.com',
    url='https://github.com/bwghughes/slinky',
    packages=[
        'slinky',
    ],
    package_dir={'slinky':
                 'slinky'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='slinky',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts':
            ['slinky=slinky:slinky']
        }
)