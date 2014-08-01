#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
]

test_requirements = [
]

setup(
    name='MPPyResponse',
    version='0.1.2',
    description='A silly Monty Python quote generator',
    long_description=readme + '\n\n' + history,
    author='Adrian Cruz',
    author_email='drincruz@gmail.com',
    url='https://github.com/drincruz/Monty-Python-PyResponse',
    packages=[
        'MPPyResponse',
    ],
    package_data={'MPPyResponse': ['monty_python.txt']},
    package_dir={'MPPyResponse':
                 'MPPyResponse'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='MPPyResponse',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
    entry_points=dict(console_scripts=['mpresponse= MPPyResponse.MPPyResponse:main']),
)
