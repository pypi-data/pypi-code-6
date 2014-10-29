#!/usr/bin/env python

# see http://bugs.python.org/issue8876
# this is just a quick hack so we can test build in vagrant
import os
if os.environ.get('USER','') == 'vagrant':
  del os.link

from setuptools import setup, find_packages

setup(name='lraudit',
      version='0.1.1',
      description='Adds auditing to LR Flask apps',
      author='Land Registry',
      author_email='lr-dev@example.org',
      url='http://github.com/LandRegistry/audit-plugin',
      packages=find_packages(exclude=['tests']),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      install_requires=[],
)
