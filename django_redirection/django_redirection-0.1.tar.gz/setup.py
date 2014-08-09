from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django_redirection',
      version=version,
      description="Redirection app by using X-Accel-Redirect",
      classifiers=["Framework :: Django","License :: OSI Approved :: MIT License","Programming Language :: Python"], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='ccat',
      author_email='',
      url='https://www.whiteblack-cat.info/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
