import os
from setuptools import setup

setup(
  name = 'import_only_py',
  version = '0.1',
  author = 'Peter Szabo',
  author_email = 'pts@fazekas.hu',
  description = (
      'Restrict imports from specific directories to .py files only.'),
  long_description = (
      'For the specified directories and their subdirectories, .pyc files '
      'will not be generated or used. Also .so (and .dll) files will be '
      'ignored.'),
  license = 'Apache License, Version 2.0',
  keywords = 'example documentation tutorial',
  url = 'https://github.com/pts/import_only_py',
  packages = [''],
  classifiers = [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 2',
      'Topic :: Software Development :: Libraries',
  ],
)
