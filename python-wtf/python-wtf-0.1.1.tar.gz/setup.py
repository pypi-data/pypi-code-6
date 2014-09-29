# -*- coding: utf-8 -*-
import os

from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

short_desc = "Debugging with print statements, but better!"
long_desc = ''
for rstfile in ('README.rst', 'HISTORY.rst', 'AUTHORS.rst'):
    if os.path.exists(rstfile):
        long_desc += open(rstfile, 'rb').read() + "\n\n"
if not long_desc:
    long_desc = short_desc

setup(
    name='python-wtf',
    version='0.1.1',
    description='Debugging with print statements, but better',
    long_description=long_desc,
    url='http://github.com/jrbl/python-wtf/',
    license='Apache 2.0',
    author='Joe Blaylock',
    author_email='jrbl@jrbl.org',
    py_modules=['wtf'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
