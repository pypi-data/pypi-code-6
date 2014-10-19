#!/usr/bin/env python
from distutils.core import setup

readme = open('README.rst').read()

setup(
    name='django-save-form',
    version='0.1.2',
    author_email='gattster@gmail.com',
    author='Philip Gatt',
    description="Encapsulate the common workflow of saving a form if "
                "submitted, displaying it if not.",
    long_description=readme,
    url='http://github.com/defcube/django-save-form/',
    py_modules=["django_save_form"],
    data_files=[('', ['README.rst'])],
    )
