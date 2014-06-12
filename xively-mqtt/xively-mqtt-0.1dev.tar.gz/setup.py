from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='xively-mqtt',
      version=version,
      description="A port of Xively library that uses MQTT instead of HTTP as data transport",
      long_description="""\
This project tries to implement a client library based on Python for Xively IoT platform. Using MQTT is expected to increase response time and save costly communication bandwidth""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mqtt xively iot m2m',
      author='Bontor Humala',
      author_email='bontorhumala@gmail.com',
      url='https://github.com/bontorhumala/xively-python',
      license='GPL',
      packages=['xively-mqtt'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'requests >= 1.1.0',
          'paho-mqtt >= 0.9.1',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
