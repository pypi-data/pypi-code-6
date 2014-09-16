#!/usr/bin/env python
from setuptools import setup

version = '0.0.2'
classifiers = ["Development Status :: 4 - Beta",
               "Environment :: Plugins",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: Apache Software License",
               "Topic :: Software Development :: Testing"]

setup(name='gcovparse',
      version=version,
      description="gcov to json",
      long_description=None,
      classifiers=classifiers,
      keywords='coverage',
      author='@codecov',
      author_email='hello@codecov.io',
      url='http://github.com/codecov/gcov-parse',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=['gcovparse'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points=None)
