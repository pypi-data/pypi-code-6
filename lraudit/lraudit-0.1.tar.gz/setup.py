#!/usr/bin/env python

# see http://bugs.python.org/issue8876
# this is just a quick hack so we can test build in vagrant
import os
if os.environ.get('USER','') == 'vagrant':
  del os.link

from setuptools import setup, find_packages

setup(name='lraudit',
      version='0.1',
      description='Adds auditing to LR Flask apps',
      author='Land Registry',
      author_email='lr-dev@example.org',
      url='http://github.com/LandRegistry/audit-plugin',
      download_url = 'http://github.com/LandRegistry/audit-plugin/tarball/alpha',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      install_requires=[],
      classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.7',
        ),
)
