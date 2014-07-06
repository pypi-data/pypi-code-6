#!/usr/bin/env python 
import os

from distutils.core import setup


setup(name='oauthclient',
      version='1.0.0',
      description='OAuth2 client library',
      author='Roberto Aguilar',
      author_email='roberto@sprocketlight.com',
      packages=['oauthclient'],
      long_description=open('README.md').read(),
      url='http://github.com/rca/oauthclient',
      license='LICENSE',
)
