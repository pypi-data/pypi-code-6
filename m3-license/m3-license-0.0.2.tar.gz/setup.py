# -*- coding: utf-8 -*-
"""
File: setup.py
Author: Rinat F Sabitov
Description: m3 license management module setup file

Tips:
 http://packages.python.org/distribute/setuptools.html
 http://diveintopython3.org/packaging.html
 http://wiki.python.org/moin/CheeseShopTutorial
 http://pypi.python.org/pypi?:action=list_classifiers
"""

import sys
import os
from setuptools import setup, find_packages

root_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root_dir, 'src'))

version = __import__('m3_license').get_version()


def read(fname):
    """ Attempt to read a file and return it's content as a text
    """
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="m3-license",
    version=version,
    description=read('DESCRIPTION'),
    keywords="django m3 bars group",

    author="BARS Group",
    author_email="bars@bars-open.ru",

    maintainer='BARS Group',
    maintainer_email='bars@bars-open.ru',

    url="http://bars-open.ru",
    package_dir={'': 'src'},
    packages=find_packages("src"),
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
    ],
    install_requires=read('REQUIREMENTS'),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    test_suite='test',
    tests_request=['nose', ]
)
