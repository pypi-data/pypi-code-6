#!/usr/bin/env python
from setuptools import setup, find_packages
import os.path

# Read README for long description
BASE = os.path.dirname(__file__)
README = os.path.join(BASE, 'README.rst')
with open(README) as f:
    long_description = f.read()


setup(name='bittivahti',
      version='0.9.2',
      description="Bittivahti bandwidth monitor for Linux",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author='Joonas Kuorilehto',
      author_email='joneskoo@kapsi.fi',
      url='https://github.com/joneskoo/bittivahti',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      bittivahti=bittivahti.cli:main
      """
      )
