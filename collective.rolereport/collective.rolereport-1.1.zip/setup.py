from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='collective.rolereport',
      version=version,
      description="Creates a report on what users have which roles",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        ],
      keywords='web zope plone',
      author='Colliberty',
      author_email='info@colliberty.com',
      url='http://www.colliberty.com/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
