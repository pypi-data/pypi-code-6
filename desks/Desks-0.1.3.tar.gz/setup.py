#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name = 'Desks'
    , version='0.1.3'
    , description='Desks to manage and drive Shelf, and provide API and data to the world'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.leloop.org/broadcast-system/desks'
    , packages = find_packages()
    , package_data = {'rest': ['config.ini']}
    , requires = ['flask_restful', 'filemagic', 'shelves', 'itsdangrous', 'flask']
    )
