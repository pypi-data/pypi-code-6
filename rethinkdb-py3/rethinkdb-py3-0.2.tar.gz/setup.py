from setuptools import setup

setup(
    name='rethinkdb-py3',
    version='0.2',
    description='Unofficial RethinkDB driver ported to Python 3',
    url='http://rethinkdb.com/',
    maintainer='Barosl Lee',
    zip_safe=True,
    packages=[
        'rethinkdb',
    ],
    entry_points={
        'console_scripts': [
            'rethinkdb-import=rethinkdb._import:main',
            'rethinkdb-export=rethinkdb._export:main',
            'rethinkdb-dump=rethinkdb._dump:main',
            'rethinkdb-restore=rethinkdb._restore:main',
        ],
    },
)
