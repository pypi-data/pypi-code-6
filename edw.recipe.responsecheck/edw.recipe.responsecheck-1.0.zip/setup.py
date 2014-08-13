# -*- coding: utf-8 -*-
"""
Installer
"""
import os
from setuptools import setup, find_packages


NAME = 'edw.recipe.responsecheck'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

entry_point = 'edw.recipe.responsecheck:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

setup(name=NAME,
      version=VERSION,
      description="A recipe that generates bash script for testing connectivity to application servers",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Zope2',
        'Framework :: Zope3',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='edw recipe zope plone connectivity server',
      package_data={'edw.recipe.responsecheck': ['*.txt', 'edw/recipe/responsecheck/*.txt']},
      author='Eau de Web',
      author_email='vitalie.maldur@eaudeweb.ro',
      url='http://github.com/eaudeweb/edw.recipe.responsecheck',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['edw', 'edw.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      entry_points=entry_points,
      )
