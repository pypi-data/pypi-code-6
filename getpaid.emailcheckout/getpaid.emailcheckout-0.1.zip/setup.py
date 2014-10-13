"""
Copyright (c) 2007 - 2008 ifPeople, Kapil Thangavelu, and Contributors
All rights reserved. Refer to LICENSE.txt for details of distribution and use.

Distutils setup

"""

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='getpaid.emailcheckout',
    version='0.1',
    license = 'ZPL2.1',
    author='Getpaid Community',
    author_email='getpaid-dev@googlegroups.com',
    description='getpaid payment processor that sends order information to the shop owner',
    long_description = (
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
        ),
    classifiers = [
        'Framework :: Zope2',
        'Framework :: Zope3',
        'Framework :: Plone'
        ],
    url='http://code.google.com/p/getpaid',
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = ['setuptools',
                        'getpaid.core',
                        'zope.interface',
                        'zope.component',
                       ],
    zip_safe = False,
    )

