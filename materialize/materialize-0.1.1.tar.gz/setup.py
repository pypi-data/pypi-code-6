#!/usr/bin/env python
from distutils.core import setup

setup(
    name='materialize',
    version='0.1.1',
    author='Shayne O\'Neill',
    author_email='shayne.oneill@dpaw.wa.gov.au',
    packages=['materialize'],
    scripts=['bin/materializer'],
    url='http://pypi.python.org/materializer',
    license='LICENSE.txt',
    description='Replace env files with etcd configurations.',
    long_description=open('README.txt').read(),
    install_requires=[
        "etcpy",
    ],
)
