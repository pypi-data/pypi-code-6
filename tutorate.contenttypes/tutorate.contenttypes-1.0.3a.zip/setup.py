from setuptools import setup, find_packages
import os

version = '1.0.3a'

setup(name='tutorate.contenttypes',
      version=version,
      description="tutorate.contenttypes",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='session,training',
      author='David Bain',
      author_email='pigeonflight@gmail.com',
      url='http://github.com/pigeonflight/tutorate.contenttypes',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tutorate'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
          'plone.app.dexterity [grok]',
          'plone.namedfile [blobs]',
          'plone.app.imagecropping',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      extras_require = {
      'test': [
            'plone.app.testing',
            'plone.app.robotframework',
            'Products.PloneTestCase',
        ],
      },


      )
