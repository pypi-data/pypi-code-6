#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.0.7'
requires = ['requests']

with open('README.rst') as f:
    readme = f.read()
    f.close()

setup(
    name='clearcache-python',
    version=version,
    description='Simple python cache clearing tool',
    long_description=readme,
    author='University of Central Florida - Marketing',
    author_email='webcom@ucf.edu',
    url='https://github.com/UCF/clearcache-python',
    packages=['clearcache'],
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
