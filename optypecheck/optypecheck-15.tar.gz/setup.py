# -*- coding: utf-8 -*-
"""
optypecheck
===========

This package implements a non intrusive and optional type checking in
functions and methods by using annotations. Once types are defined in
annotations, no changes are required to make the verification of types.
And, because it is completely optional, it can be used only in the
desired environments, like unit testings. This way, the performance of
production code is not affected.

Learn more in:

    https://bitbucket.org/carlopires/optypecheck


Installation
------------

.. code:: bash

    pip3 install optypecheck

Example
-------

.. code:: python

    def gencode(a: bytes, b: str) -> str:
        return '{}{}'.format(a[0], b)

    def valid_number(n) -> 'decimal.Decimal':
        return n

    # enable type checking in DEBUG mode
    assert __import__('typecheck').typecheck(__name__)

"""
from setuptools import setup

setup(
    name='optypecheck',
    version=15,
    url='https://bitbucket.org/carlopires/optypecheck',
    author='Carlo Pires',
    author_email='carlopires@gmail.com',
    description='A non intrusive and optional *type checking for Python 3* '
                'using annotations',
    long_description=__doc__,
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
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    test_suite='test.suite',
)
