import sys
from setuptools import setup

install_requires = [
    'argparse',
    'virtualenv',
    'six'
]

classifiers = [
    'Programming Language :: Python :: {0}'.format(py_version)
    for py_version in ['2.7', '3.4']]
classifiers.extend([
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Environment :: Console',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
])


setup(
    name = 'cassandra-quickstart',
    version = '0.1',
    description = 'Quickstart tool for installing and managing Cassandra in development environments',
    author = 'Ryan McGuire',
    author_email = 'ryan@datastax.com',
    url = 'https://github.com/EnigmaCurry/cassandra-quickstart',
    install_requires = install_requires,
    packages=["cassandra_quickstart"],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['cassandra-quickstart = cassandra_quickstart.main:main', 'cqs = cassandra_quickstart.main:main']},
)
