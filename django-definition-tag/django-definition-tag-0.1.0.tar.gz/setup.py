#!/usr/bin/env python
from distutils.core import setup

readme = open('README.rst').read()

setup(
    name='django-definition-tag',
    version='0.1.0',
    author_email='gattster@gmail.com',
    author='Philip Gatt',
    description="Allows easy creation of template tags that define a context variable",
    long_description=readme,
    url='http://github.com/defcube/django-definition-tag/',
    py_modules=["django_definition_tag"],
    data_files=[('', ['README.rst'])],
    )