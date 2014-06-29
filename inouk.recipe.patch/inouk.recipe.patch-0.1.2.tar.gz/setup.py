# -*- coding: utf-8 -*-
"""
This module contains the tool inouk.recipe.patch
"""
import os
from setuptools import setup, find_packages

name = "inouk.recipe.patch"
version = '0.1.2'

long_description = (
    '\nDetailed Documentation\n'
    '======================\n'
    + '\n' +
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    'Change history\n'
    '==============\n'
    + '\n' +
    open('CHANGES.txt').read()
    + '\n'
)

entry_point = '%s:Recipe' % name

setup(
    name=name,
    version=version,
    description="A buildout recipe for patching mainly designed to work with anybox.openerp.recipe",
    long_description=long_description,
    
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
    ],
    keywords='buildout patch',
    author=('Cyril MORISSE'),
    author_email='cmorisse at boxes3.net',
    url='http://bitbucket.org/cmorisse/inouk-recipe-patch',
    license='LGPL',
    packages=find_packages(), 
    namespace_packages=['inouk', 'inouk.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',],
    entry_points = {
        'zc.buildout': ["default = %s" % entry_point],
        'zc.buildout.uninstall': ["default = %s:uninstall_recipe" % name]
    },
)
