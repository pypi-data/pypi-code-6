#!/usr/bin/env python

from setuptools import setup
setup(
  name = 'django-wham',
  packages = ['wham'],
  version = '0.1.0',
  description = 'Rest APIs disguised as Django ORM Models',
  author = 'Michael Bylstra',
  author_email = 'mbylstra@gmail.com',
  url = 'https://github.com/mbylstra/django-wham',
  install_requires = ['django', 'requests']
)