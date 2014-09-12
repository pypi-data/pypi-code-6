#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='featurevectormatrix',
    version='0.1.0',
    description='Python class to encapsulate different representations of large datasets',
    long_description=readme + '\n\n' + history,
    author='Jeremy Robin',
    author_email='jeremy.robin@gmail.com',
    url='https://github.com/talentpair/featurevectormatrix',
    packages=[
        'featurevectormatrix',
    ],
    package_dir={'featurevectormatrix':
                 'featurevectormatrix'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='featurevectormatrix',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)