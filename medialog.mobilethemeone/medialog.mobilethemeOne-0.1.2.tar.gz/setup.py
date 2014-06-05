from setuptools import setup, find_packages
import os

version = '0.1.2'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n')

setup(name='medialog.mobilethemeOne',
      version=version,
      description="A diazo theme for zettwerk.mobiletheming",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='mobiletheming plone zetterk',
      author='Espen Moe-Nilssen',
      author_email='',
      url='http://github.com/espenmn/medialog.mobilethemeOne',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['medialog'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'ftw.mobilenavigation',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
