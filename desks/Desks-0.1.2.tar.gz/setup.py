#!/usr/bin/env python

from distutils.core import setup

setup(name = 'Desks'
    , version='0.1.2'
    , description='Desks to manage and drive Shelf, and provide API and data to the world'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.leloop.org/broadcast-system/desks'
    , packages = ['rest', 'rest.resources', 'rest.common']
    , package_data = {'rest': ['config.ini']}
    , requires = ['flask_restful', 'filemagic', 'shelves', 'itsdangrous', 'flask']
    )
