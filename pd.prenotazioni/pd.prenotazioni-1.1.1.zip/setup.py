# -*- coding: utf-8 -*-
"""
This module contains the tool of pd.prenotazioni
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.1.1'

long_description = (
    read('README.rst')
    + '\n' +
    'Change history\n'
    '**************\n\n'
    + '\n' +
    read('CHANGES.rst')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing']

setup(
    name='pd.prenotazioni',
    version=version,
    description=(
        "pd.prenotazioni: a Plone product for booking"
    ),
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
    ],
    keywords='',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='http://svn.plone.org/svn/collective/',
    license='gpl',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['pd'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'pd.contentrules.sms',
        'plone.api',
        'rg.prenotazioni>=3.3.0.dev0',
        'z3c.pdftemplate'
    ],
    tests_require=tests_require,
    extras_require=dict(test=tests_require),
    test_suite='pd.prenotazioni.tests.test_docs.test_suite',
    entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
