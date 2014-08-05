#!/usr/bin/env python
# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
from gzipper.version import __version__


PROJECT = 'hyde-gzipper'
try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''


setup(name=PROJECT,
      version=__version__,
      description='Hyde plugin for gzipping files',
      long_description = long_description,
      author='Radek Czajka',
      author_email='rczajka@rczajka.pl',
      url='http://rczajka.pl/hyde-gzipper',
      packages=find_packages(),
      requires=['python (>= 2.7)'],
      license='MIT',
      classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Site Management',
        ],
      zip_safe=True,
)
