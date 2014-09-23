#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pelican_git


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

packages = [
    'pelican_git',
]

requires = [
    "setuptools",
    'requests>=2.2.0',
    'beautifulsoup',
    'jinja2',
]

tests_require = [
    'mock>=1.0.1'
]

setup(
    name='pelican-git',
    version=pelican_git.__version__,
    description='Easily embed GitHub Git file in your Pelican articles.',
    long_description=readme,
    author='Ha.Minh',
    author_email='minhhh@minhhuyha.info',
    url='https://github.com/minhhh/pelican-git',
    packages=packages,
    package_data={'': ['LICENSE', ],
                    'pelican_git': ['templates/*.jinja.html']},
    package_dir={'pelican_git': 'pelican_git'},
    include_package_data=True,
    install_requires=requires,
    tests_require=tests_require,
    license='MIT',
    zip_safe=False,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ),
)
