#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""This file is for distribute yatel with distutils

"""

#==============================================================================
# CONSTANTS
#==============================================================================

REQUIREMENTS = [
    "Flask>=0.10.1", "Flask-Script>=2.0.5", "SQLAlchemy>=0.9.7",
    "jsonschema>=2.4.0", "requests>=2.4.0", "mock>=1.0.1",
    "numpy>=1.8.2", "scipy>=0.14.0"
]


#==============================================================================
# FUNCTIONS
#==============================================================================

if __name__ == "__main__":
    import os
    import sys

    from ez_setup import use_setuptools
    use_setuptools()

    from setuptools import setup, find_packages

    import yatel

    setup(
        name=yatel.PRJ.lower(),
        version=yatel.STR_VERSION,
        description=yatel.SHORT_DESCRIPTION,
        author=yatel.AUTHOR,
        author_email=yatel.EMAIL,
        url=yatel.URL,
        license=yatel.LICENSE,
        keywords=yatel.KEYWORDS,
        classifiers=yatel.CLASSIFIERS,
        packages=[pkg for pkg in find_packages() if pkg.startswith("yatel")],
        include_package_data=True,
        py_modules=["ez_setup"],
        entry_points={'console_scripts': ['yatel = yatel.cli:main']},
        install_requires=REQUIREMENTS,
    )
