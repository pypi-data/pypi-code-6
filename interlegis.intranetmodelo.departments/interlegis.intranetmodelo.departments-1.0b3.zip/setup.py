# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0b3'
description = 'Implementa departamentos dentro de uma Intranet Modelo do Programa Interlegis'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='interlegis.intranetmodelo.departments',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='interlegis intranet portalmodelo plone',
    author='Programa Interlegis',
    author_email='ti@interlegis.leg.br',
    url='https://github.com/interlegis/interlegis.intranetmodelo.departments',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interlegis', 'interlegis.intranetmodelo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Acquisition',
        'five.grok',
        'plone.api',
        'plone.app.dexterity [grok]',
        'plone.app.referenceablebehavior',
        'plone.dexterity',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'sc.contentrules.group',
        'sc.contentrules.localrole',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'plone.uuid',
            'zope.component',
        ],
    },
    entry_points='''
      [z3c.autoinclude.plugin]
      target = plone
      ''',
)
