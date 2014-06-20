#!/usr/bin/env python

from distutils.core import setup

setup(name='SmartUPS',
    version='1.0',
    description='SmartUPS library',
    author='openelectrons.com',
    author_email='contact@openelectrons.com',
    url='http://www.openelectrons.com/index.php?module=pagemaster&PAGE_user_op=view_page&PAGE_id=33',
    py_modules=['smartups'],
    install_requires=['OpenElectrons_i2c'],
    )