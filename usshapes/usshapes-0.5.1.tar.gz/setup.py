#!/usr/bin/env python
from setuptools import setup

setup(name='usshapes',
      version='0.5.1',
      description='Create an Elasticsearch index of United States shapefiles, and generate a suggestions index for those locations',
      author='Daniel Sarfati',
      author_email='daniel@knockrentals.com',
      url='https://github.com/fatisar/us-shapes',
      scripts=['bin/us-shapes.py'],
      packages=['usshapes'],
      install_requires=['pyes', 'beautifulsoup4', 'requests']
)
