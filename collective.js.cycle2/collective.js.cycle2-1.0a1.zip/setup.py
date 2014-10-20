# -*- coding:utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0a1'
description = 'Integration of Cycle2 jQuery plugin in Plone.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.js.cycle2',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone jquery plugin cycle2 slideshow',
    author='Simples Consultoria',
    author_email='produtos@simplesconsultoria.com.br',
    url='https://github.com/collective/collective.js.cycle2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective', 'collective.js'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.CMFPlone >=4.2',
        'Products.GenericSetup',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
