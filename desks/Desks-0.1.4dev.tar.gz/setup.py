#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'Desks'
    , version='0.1.4dev'
    , description='Desks to manage and drive Shelf, and provide API and data to the world'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.leloop.org/broadcast-system/desks'
    , packages = find_packages()
    , requires = ['flask_restful', 'flask_cors', 'filemagic', 'shelves', 'itsdangerous']
    , entry_points = {
            "console_scripts": [
                "dskConfig = rest.api:config",
                "dskRun = rest.api:run",
            ]
        }
    )
