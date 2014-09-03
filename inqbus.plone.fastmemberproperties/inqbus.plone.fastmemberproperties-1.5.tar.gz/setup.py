from setuptools import setup, find_packages
import os

version = '1.5'

setup(name='inqbus.plone.fastmemberproperties',
      version=version,
      description="Provide methods to get meta data like email, fullname aso. fast as possible even for many members.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone,zope,member',
      author='Maik Derstappen',
      author_email='md@derico.de.de',
      url='http://inqbus-hosting.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['inqbus', 'inqbus.plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
