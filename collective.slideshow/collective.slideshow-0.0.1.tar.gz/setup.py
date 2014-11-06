from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(name='collective.slideshow',
      version=version,
      description="Adds slideshow folder to all folderish items.",
      long_description=open("README.txt").read() + "\n" +
                       open("docs/HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='slideshow',
      author='Andre Goncalves',
      author_email='andre@intk.com',
      url='https://github.com/intk/collective.slideshow',
      download_url='https://github.com/intk/collective.slideshow/tarball/0.0.1',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
