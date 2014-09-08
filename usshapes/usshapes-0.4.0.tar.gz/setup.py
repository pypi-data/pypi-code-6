#!/usr/bin/env python
from setuptools import setup

setup(name='usshapes',
      version='0.4.0',
      description='U.S. Shapefile Indexer for Elasticsearch',
      author='Daniel Sarfati',
      author_email='daniel@knockrentals.com',
      url='https://github.com/fatisar/us-shapes',
      scripts=['bin/run.py'],
      packages=['usshapes'],
      install_requires=['pyes', 'beautifulsoup4', 'requests']
)
