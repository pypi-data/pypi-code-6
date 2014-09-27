#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

from setuptools import setup


with open('README.rst') as f:
    readme = f.read()


setup(
    name='warouter',
    version='0.0.2',
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    url='https://github.com/remcohaszing/python-warouter',
    description='Warouter is a simple routing wrapper around webapp2.',
    long_description=readme,
    license='MIT',
    py_modules=['warouter'],
    install_requires=[
        'webapp2',
        'webob'
    ],
    test_suite='tests',
    zip_safe=True)
