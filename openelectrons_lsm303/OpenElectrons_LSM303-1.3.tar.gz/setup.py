#!/usr/bin/env python

from distutils.core import setup

setup(name='OpenElectrons_LSM303',
    version='1.3',
    description='OpenElectrons LSM303 library',
    author='openelectrons.com',
    author_email='contact@openelectrons.com',
    url='http://www.openelectrons.com/index.php?module=pagemaster&PAGE_user_op=view_page&PAGE_id=62',
    py_modules=['OpenElectrons_LSM303'],
    install_requires=['OpenElectrons_i2c'],
    )