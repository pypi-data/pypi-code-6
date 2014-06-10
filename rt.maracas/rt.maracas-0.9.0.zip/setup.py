# -*- coding: utf-8 -*-
"""Installer for the rt.maracas package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = "\n\n".join((
    read('README.rst'),
    read('docs', 'CHANGELOG.rst')
))

setup(
    name='rt.maracas',
    version='0.9.0',
    description="A Plone gadget for the 2014 FIFA World Cup Brazil",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    keywords='Plone',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='http://pypi.python.org/pypi/rt.maracas',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['rt'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
