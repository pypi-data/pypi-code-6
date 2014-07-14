# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2.1'

long_description = (
    read('README.txt')
    + '\n\n' +
    read('CHANGES.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing']

setup(name='zettwerk.mailtemplates',
      version=version,
      description="Create and send mail templates in plone.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='Plone',
      author='Jörg Kubaile / zettwerk GmbH',
      author_email='jk@zettwerk.com',
      url='http://zettwerk.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zettwerk', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        'z3c.jbot',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='zettwerk.mailtemplates.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
