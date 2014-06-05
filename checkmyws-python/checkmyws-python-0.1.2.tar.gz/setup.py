#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import distribute_setup
    distribute_setup.use_setuptools()
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import re

with open(os.path.join(os.path.dirname(__file__),
                       'checkmyws',
                       '__init__.py')) as f:
        data = f.read()

        version = re.search("__version__ = \"(.*)\"", data).group(1)
        license = re.search("__license__ = \"(.*)\"", data).group(1)
        author = re.search("__author__ = \"(.*)\"", data).group(1)
        author_email = re.search("__author_email__ = \"(.*)\"", data).group(1)
        description = re.search("__description__ = \"(.*)\"", data).group(1)
        url = re.search("__url__ = \"(.*)\"", data).group(1)

with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

with open('test-requirements.txt', 'r') as f:
    test_requires = [x.strip() for x in f if x.strip()]

setup(
    name='checkmyws-python',
    url=url,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    license=license,
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    tests_require=test_requires,
    install_requires=requires,
    extras_require={'test': test_requires},
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ),
)
