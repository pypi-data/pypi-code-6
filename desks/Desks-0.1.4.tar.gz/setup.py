#!/usr/bin/env python

from setuptools import setup

setup(name = 'Desks'
    , version='0.1.4'
    , description='Desks to manage and drive Shelf, and provide API and data to the world'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.leloop.org/broadcast-system/desks'
    , packages = ['rest', 'rest.common', 'rest.resources']
    , package_dir = {'rest': 'rest'}
    , package_data = {'rest': ['config.ini']}
    , requires = ['flask_restful', 'filemagic', 'shelves', 'itsdangerous']
    , entry_points = {
            "console_scripts": [
                "dskConfig = rest.api:config",
            ]
        }
    )
