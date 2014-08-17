#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name = 'Shelves'
    , version='0.3.8'
    , description='Shelves to store Box of documents in the brodacast-system'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.leloop.org/broadcast-system/shelves'
    , packages = find_packages()
    , requires = ['tahoe_whoosh', 'whoosh', 'requests']
    )
