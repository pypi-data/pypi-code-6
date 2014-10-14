# coding: utf-8
from setuptools import setup


setupargs = {
    'name': 'myorm',
    'description': 'Provides a more or less simple ORM for MySQL and SQLite (PostgreSQL support is planned).',

    'license': 'GPLv3',
    'version': '0.2',

    'packages': ['myorm'],

    'install_requires': [
        'flask',
    ],

    'author': 'Christian Kokoska',
    'author_email': 'hoschi@eternalconcert.de',
}

if __name__ == '__main__':
    setup(**setupargs)
