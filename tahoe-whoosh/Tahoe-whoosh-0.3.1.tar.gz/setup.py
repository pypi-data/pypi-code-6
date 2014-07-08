#!/usr/bin/env python

from distutils.core import setup

setup(name = 'Tahoe-whoosh'
    , version='0.3.1'
    , description='Using and storing whoosh index in Tahoe LAFS grid'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.leloop.org/okhin/tahoe-whoosh/'
    , py_modules = ['tahoe_whoosh']
    , requires = ['whoosh', 'requests']
    )
