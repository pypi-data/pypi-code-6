#!/usr/bin/env python

from setuptools import setup

with open('./requirements.txt') as requirements_txt:
    requirements = [line for line in requirements_txt]

description = 'Manage static files in Django with r.js, '
description += 'serve from Rackspace Cloud files'

setup(name='django-require-cumulus',
      version='0.2',
      description=description,
      author='Paris Kasidiaris',
      author_email='pariskasidiaris@gmail.com',
      url='https://github.com/sourcelair/django-require-cumulus',
      packages=['require_cumulus'],
      install_requires=requirements,
      license=open('LICENSE').read())
