from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='browserstack',
      version=version,
      description="Unofficial Python Library for Browserstack",
      long_description="""\
Unofficial Python Library for Browserstack""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python browserstack',
      author='Vibhaj Rajan',
      author_email='vibhaj8@gmail.com',
      url='https://github.com/tr4n2uil/python-browserstack',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
