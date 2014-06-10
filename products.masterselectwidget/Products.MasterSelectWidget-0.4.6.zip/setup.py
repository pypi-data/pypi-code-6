import os
import sys
from setuptools import setup, find_packages

version = '0.4.6'

if sys.version_info[0] == 2 and sys.version_info[1] < 6:
    requires = ['simplejson']
else:
    requires = []

setup(name='Products.MasterSelectWidget',
      version=version,
      description="An Archetypes widget that controls the vocabulary or "
            "display of otheer fields on an edit page",
      long_description=open("README.rst").read() + "\n" + 
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Plone Collective',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://plone.org/products/masterselectwidget/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ] + requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
