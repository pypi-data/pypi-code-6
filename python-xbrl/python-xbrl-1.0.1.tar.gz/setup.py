import re
import sys

from distutils.core import setup

setup(
    name='python-xbrl',
    version='1.0.1',
    description='library for parsing xbrl documents',
    author='Joe Cabrera',
    author_email='jcabrera@eminorlabs.com',
    license='Apache License',
    keywords='xbrl, Financial, Accounting, file formats',
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Topic :: Office/Business :: Financial',
    ],
    scripts=['python-xbrl/python-xbrl.py'],
    url='https://github.com/greedo/python-xbrl/',
)
