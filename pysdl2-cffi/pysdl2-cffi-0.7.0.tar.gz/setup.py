#!/usr/bin/env python

from setuptools import setup

import codecs
README = codecs.open('README.rst', encoding='utf-8').read()
CHANGES = codecs.open('CHANGES.rst', encoding='utf-8').read()

setup(name="pysdl2-cffi",
    version = "0.7.0",
    packages = [ 'sdl', '_sdl', '_sdl_image', '_sdl_mixer', '_sdl_ttf' ],
    install_requires = [ 'cffi', 'apipkg' ],
    extras_require = {'build':['pycparser']},
    description = "SDL2 wrapper with cffi",
    long_description = README + CHANGES,
    license = "GPLv2+",
    classifiers = [
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)"
	],
    keywords = ['sdl', 'cffi'],
    author="Daniel Holth",
    author_email="dholth@fastmail.fm",
    url="https://bitbucket.org/dholth/pysdl2-cffi")
