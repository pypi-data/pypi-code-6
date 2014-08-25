# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0b2'
description = 'Portal Modelo: Integração com sistemas do processo legislativo.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='interlegis.portalmodelo.pl',
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
    keywords='interlegis sapl plone portalmodelo plone',
    author='Programa Interlegis',
    author_email='ti@interlegis.leg.br',
    url='https://github.com/interlegis/interlegis.portalmodelo.pl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interlegis', 'interlegis.portalmodelo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.z3cform.datagridfield',
        'collective.z3cform.datetimewidget',
        'five.grok',
        'interlegis.portalmodelo.api',
        'plone.api',
        'plone.app.contentmenu',
        'plone.app.dexterity [grok, relations]',
        'plone.app.referenceablebehavior',
        'plone.app.registry',
        'plone.app.relationfield',
        'plone.autoform',
        'plone.dexterity',
        'plone.directives.dexterity',
        'plone.directives.form',
        'plone.formwidget.contenttree',
        'plone.memoize',
        'plone.namedfile',
        'plone.registry',
        'plone.supermodel',
        'Products.CMFCore',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'z3c.form',
        'z3c.relationfield',
        'zc.relation',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.intid',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'plone.api',
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'plone.uuid',
            'robotsuite',
        ],
    },
    entry_points='''
      [z3c.autoinclude.plugin]
      target = plone
      ''',
)
