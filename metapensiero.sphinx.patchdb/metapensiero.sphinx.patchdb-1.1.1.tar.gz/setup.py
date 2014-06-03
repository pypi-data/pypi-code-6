# -*- coding: utf-8 -*-
# :Progetto:  metapensiero.sphinx.patchdb
# :Creato:    sab 22 ago 2009 17:26:36 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt')) as f:
    VERSION = f.read().strip()

setup(
    name='metapensiero.sphinx.patchdb',
    version=VERSION,
    description="Extract scripts from a reST document and apply them in order.",
    long_description=README + '\n\n' + CHANGES,

    author='Lele Gaifax',
    author_email='lele@metapensiero.it',
    url="https://bitbucket.org/lele/metapensiero.sphinx.patchdb",

    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Database",
        ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['metapensiero', 'metapensiero.sphinx'],

    install_requires=[
        'PyYAML',
        'setuptools',
        'sqlalchemy',
        ],
    extras_require={'dev': ['docutils', 'pygments', 'sphinx']},

    tests_require=[
        'docutils',
        'nose',
        'pygments',
        'sphinx',
    ],
    test_suite='nose.collector',

    entry_points="""\
    [console_scripts]
    patchdb = metapensiero.sphinx.patchdb.pup:main
    dbloady = metapensiero.sphinx.patchdb.dbloady:main
    """,
)
