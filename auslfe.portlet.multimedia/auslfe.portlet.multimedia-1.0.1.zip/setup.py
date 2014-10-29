from setuptools import setup, find_packages
import os

version = '1.0.1'
tests_require = ['plone.app.testing']

setup(name='auslfe.portlet.multimedia',
      version=version,
      description="A simple Plone multimedia Portlet with an eye to accessibility",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Development Status :: 5 - Production/Stable",
        ],
      keywords='plone jquery plonegov portlet multimedia image',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturte.it',
      url='http://plone.org/products/auslfe.portlet.multimedia',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['auslfe', 'auslfe.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'collective.js.imagesloaded',
      ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
