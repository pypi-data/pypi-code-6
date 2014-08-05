#!/usr/bin/env python

from distutils.core import setup

setup(name='OpenElectrons_IMUbreakout',
    version='1.0',
    description='OpenElectrons IMUbreakout library',
    author='openelectrons.com',
    author_email='contact@openelectrons.com',
    url='http://www.openelectrons.com/index.php?module=pagemaster&PAGE_user_op=view_page&PAGE_id=62',
    py_modules=['OpenElectrons_LSM303D', 'OpenElectrons_L3GD20', 'OpenElectrons_BMP180'],
    install_requires=['OpenElectrons_i2c'],
    )