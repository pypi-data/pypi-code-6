#!/usr/bin/env python
from distutils.core import setup

setup(
    name='ldap_paged_search',
    version='0.2',
    packages=['ldap_paged_search'],
    license='LGPLv2.1',
    description='Easily perform LDAP queries with more than 1000 results',
    author='Michael Henry a.k.a. neoCrimeLabs',
    author_email='mhenry@neocri.me',
    url='https://github.com/neoCrimeLabs/python-ldap_paged_search',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP']
    )
