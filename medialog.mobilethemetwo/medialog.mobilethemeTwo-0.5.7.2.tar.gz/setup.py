from setuptools import setup, find_packages
import os

version = '0.5.7.2'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n')

setup(name='medialog.mobilethemeTwo',
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
      author_email='espen@medialog.no',
      url='http://github.com/espenmn/medialog.mobilethemeTwo',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['medialog'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.z3cform.datagridfield',
          'cssselect',
          'ftw.mobilenavigation',
          'medialog.controlpanel',
          'plone.api',
          'plone.app.themingplugins',
          'plone.directives.form',
          'requests',
          'z3c.jbot',
          'zettwerk.mobiletheming',
          'plone.behavior'

          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
