#!/usr/bin/env python

from distutils.core import setup

setup(name = 'Shelves'
    , version='0.2.1'
    , description='Shelves to store Box of documents in the brodacast-system'
    , author='Okhin'
    , author_email='okhin@okhin.fr'
    , url='https://git.leloop.org/broadcast-system/shelves'
    , packages = ['shelves']
    , requires = ['tahoe_whoosh', 'whoosh', 'requests']
    )
