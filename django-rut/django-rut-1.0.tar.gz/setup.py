#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name='django-rut',
      version='1.0',
      description='A simple Django template filter to format/unformat Chilean RUT',
      author='Eduardo Oyarzún',
      author_email='',
      url='',
      packages=['django_rut', 'django_rut.templatetags'],
     )