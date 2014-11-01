# -*- coding: utf-8 -*-

from setuptools import setup
import twipy

REQUIREMENTS = ['oauth2']
TEST_REQUIREMENTS = ['nose', 'coveralls', 'coverage']

LONG_DESCRIPTION = """
Twipy is a Twitter application for the Unix/Linux console and it's written in Python 2.7
"""

SHORT_DESCRIPTION = 'Another Twitter client using Python 2.7'

setup(name='twipy',
      version=twipy.version,
      packages=['twipy'],
      description=SHORT_DESCRIPTION,
      author='Victor Martin',
      author_email='vitomarti@gmail.com',
      url='https://github.com/ervitis/twipy',
      keywords='twitter client console',
      zip_safe=True,
      entry_points={
          'console_scripts': ['twipy = twipy.main:main']
      },
      download_url='https://github.com/ervitis/twipy/tarball/' + twipy.version,
      license='MIT',
      install_requires=REQUIREMENTS,
      tests_require=TEST_REQUIREMENTS,
      long_description=LONG_DESCRIPTION,
      classifiers=[])
