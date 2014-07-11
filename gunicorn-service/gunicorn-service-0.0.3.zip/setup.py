#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gunicorn_service
from setuptools import setup

description = 'let gunicorn easy install as a service'

setup(name='gunicorn-service',
      version=gunicorn_service.__version__,
      description=description,
      long_description=open('./README.rst', 'r').read(),
      author="MaxiL",
      author_email='maxil@interserv.com.tw',
      url='https://github.com/maxi119/gunicorn_service',
      packages=['gunicorn_service'],
      download_url="https://github.com/maxi119/gunicorn_service",
      keywords="gunicorn service",
      classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
     )
