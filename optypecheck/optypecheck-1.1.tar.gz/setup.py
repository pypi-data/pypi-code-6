# -*- coding: utf-8 -*-
"""
Created on 27/06/2014
@author: Carlo Pires <carlopires@gmail.com>
"""
from setuptools import setup

def get_version():
    from typecheck import __version__
    return __version__

def get_long_description():
    with open('README.pypi') as readme:
        return readme.read()

setup(
    name='optypecheck',
    version=get_version(),
    url='https://bitbucket.org/carlopires/optypecheck',
    author='Carlo Pires',
    author_email='carlopires@gmail.com',
    description='A non intrusive optional type checking for Python 3 using annotations',
    long_description=get_long_description(),
    zip_safe=True,
    packages=['typecheck'],
    platforms='any',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test.suite',
)
