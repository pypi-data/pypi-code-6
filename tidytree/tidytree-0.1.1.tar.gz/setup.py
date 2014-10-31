# -*- coding: UTF-8 -*-

import setuptools
from distutils.core import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='tidytree/__init__.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

setup(
    name='tidytree',
    version=verstr,
    author='Salmon Thomas',
    author_email='ths871@gmail.com',
    packages=['tidytree'],
    url='https://github.com/tsalmon/tidytree',
    license=open('LICENSE', 'r').read(),
    description='manager directories',
    long_description=open('README.md', 'r').read(),
    install_requires=[
        'requests >= 2.3.0',
        'argparse >= 1.1',
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts':[
            'tidytree = tidytree.cli:main'
        ]
    },
)
