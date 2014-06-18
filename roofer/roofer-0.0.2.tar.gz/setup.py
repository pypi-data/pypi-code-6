#!/usr/bin/env python
# -*- coding: utf8 -*-

"""setup
(C) Franck Barbenoire <contact@franck-barbenoire.fr>
License : GPL v3"""

from distutils.core import setup

import roofer

setup(name = "roofer",
    version = roofer.__version__,
    description = ".",
    author = "Franck Barbenoire",
    author_email = "contact@franck-barbenoire.fr",
    url = "https://github.com/franckinux/roofer",
    py_modules=["roofer"],
    install_requires = ['Pillow',],
    classifiers = ['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'Topic :: Multimedia :: Graphics :: Graphics Conversion']
)
