#!/usr/bin/env python

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'VERSION.txt'), 'r') as v:
    version = v.read().strip()

with open(os.path.join(here, 'REQUIREMENTS.txt'), 'r') as r:
    requires = r.read().split()

with open(os.path.join(here, 'README.rst'), 'r') as r:
    readme = r.read()

download_url = 'https://github.com/amigocloud/python-amigocloud/tarball/%s'


setup(
    name='amigocloud',
    packages=['amigocloud'],
    version=version,
    description='Python client for the AmigoCloud REST API',
    long_description=readme,
    author='Julio M Alegria',
    author_email='julio@amigocloud.com',
    url='https://github.com/amigocloud/python-amigocloud',
    download_url=download_url % version,
    install_requires=requires,
    license='MIT'
)
