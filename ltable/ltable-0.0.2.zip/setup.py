#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ltable
from setuptools import setup

description = 'lite table, not depden on numpy or sqlite' + \
              'operations,.. find, filter, group, sort, top, tail ..'

setup(name='ltable',
      version=ltable.__version__,
      description=description,
      long_description=open('./README', 'r').read(),
      author="MaxiL",
      author_email='maxil@interserv.com.tw',
      url='https://github.com/maxi119/python-ltable',
      packages=['ltable'],
      download_url="https://github.com/maxi119/python-ltable",
      keywords="lightning table",
      classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
     )
