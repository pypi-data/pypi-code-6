#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="autodebug",
    version="0.9",
    author="Michał Podeszwa",
    author_email="michal.podeszwa@gmail.com",
    description=("Importing this module enables automatic post mortem debugging"
                 " upon any exception. It uses module specified in envvar"),
    license="BSD",
    keywords="debugger debug automatic auto auto-debug",
    packages=["auto_debug"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Debuggers'
    ]
)
