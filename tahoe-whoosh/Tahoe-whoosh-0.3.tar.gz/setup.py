#!/usr/bin/env python

from distutils.core import setup

setup(name = 'Tahoe-whoosh'
    , version='0.3'
    , description='Using and storing whoosh index in Tahoe LAFS grid'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.okhin.fr/?p=okhin/tahoe-whoosh.git'
    , py_modules = ['tahoe_whoosh']
    , requires = ['whoosh', 'requests']
    )
