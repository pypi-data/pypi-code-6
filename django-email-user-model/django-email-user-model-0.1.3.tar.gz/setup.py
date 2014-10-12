#!/usr/bin/env python
# encoding: utf-8

import setuptools
from setuptools import setup, find_packages

import django_email_user_model


setup(name='django-email-user-model',
      version=django_email_user_model.__version__,
      description="Django custom user model that enable E-Mail as username",
      author="Jeff Buttars",
      author_email="jeffbuttars@gmail.com",
      packages=find_packages(),
      license='MIT',
      package_dir={'django_email_user_model': 'django_email_user_model'},
      install_requires=[
          'Django',
      ],
      # data_files=[
      #     ('/etc/init.d', ['conf/init.d/afile']),
      # ],
      )
