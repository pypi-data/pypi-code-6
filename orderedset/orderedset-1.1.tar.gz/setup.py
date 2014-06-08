#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
from setuptools import setup, find_packages, Extension


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def read_reqs(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return [line for line in f.read().split('\n') if line and not line.strip().startswith('#')]


def read_version():
    with open(os.path.join('lib', 'orderedset', '__init__.py')) as f:
        m = re.search(r'''__version__\s*=\s*['"]([^'"]*)['"]''', f.read())
        if m:
            return m.group(1)
        raise ValueError("couldn't find version")


try:
    from Cython.Build import cythonize
    extensions = cythonize(Extension('orderedset._orderedset',
                                     ['lib/orderedset/_orderedset.pyx']))
except ImportError:
    # couldn't import Cython, try with the .c file
    extensions = [Extension('orderedset._orderedset',
                            ['lib/orderedset/_orderedset.c'])]


tests_require = []
if sys.version_info < (2, 7):
    tests_require.append("unittest2")


# NB: _don't_ add namespace_packages to setup(), it'll break
#     everything using imp.find_module
setup(
    name='orderedset',
    version=read_version(),
    description='An Ordered Set implementation in Cython.',
    long_description=readme + '\n\n' + history,
    author='Simon Percivall',
    author_email='percivall@gmail.com',
    url='https://github.com/simonpercivall/orderedset',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    ext_modules=extensions,
    include_package_data=True,
    install_requires=read_reqs('requirements.txt'),
    license="BSD",
    zip_safe=False,
    keywords='orderedset',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    tests_require=tests_require,
    test_suite='tests',
    timeit_suite='timings',
)
