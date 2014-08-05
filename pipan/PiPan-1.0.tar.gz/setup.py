#!/usr/bin/env python

from distutils.core import setup

setup(name='PiPan',
    version='1.0',
    description='OpenElectrons Pi-Pan library',
    author='openelectrons.com',
    author_email='contact@openelectrons.com',
    url='http://www.openelectrons.com/index.php?module=pagemaster&PAGE_user_op=view_page&PAGE_id=15',
    py_modules=['pilight', 'pipan'],
    install_requires=['OpenElectrons_i2c'],
    )