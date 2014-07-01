# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.2.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='zettwerk.mobile',
      version=version,
      description="jquery.mobile based themes for plone.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone, theme, jquery, jquery.mobile',
      author='Jörg Kubaile / zettwerk GmbH',
      author_email='jk@zettwerk.com',
      url='http://www.zettwerk.com',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['zettwerk'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zettwerk.mobiletheming>=0.2',
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
