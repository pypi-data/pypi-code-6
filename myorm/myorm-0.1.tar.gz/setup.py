# coding: utf-8
from setuptools import setup


setupargs = {
    'name': 'myorm',
    'description': 'My private ORM',

    'license': 'GPLv3',
    'version': '0.1',

    'packages': ['myorm'],

    'install_requires': [
        'flask',
    ],

    'author': 'Christian Kokoska',
    'author_email': 'hoschi@eternalconcert.de',
}

if __name__ == '__main__':
    setup(**setupargs)
