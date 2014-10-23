#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8

from setuptools import setup, find_packages
import sys
from easy_contact import version
import os

# Read the version from a project file
VERSION = version.VERSION_str

# Get description from README file
long_description = open(
                os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Build a list with requirements of the app
REQUIRES = []
try:
    import django
except ImportError:
    # Because of the strange update behavior of "pip --upgrade package_name"
    # set requierment only if django not avallible.
    REQUIRES.append('django')

if sys.version_info < (2, 4):
    REQUIRES.append('python >= 2.4')


setup(name='django-easy-contact',
      version=VERSION,
      description='A simple contact form application.',
      long_description=long_description,
      author='Andreas Fritz, digital.elements.li',
      author_email='easy-contact@bitzeit.eu',
      url='https://bitbucket.org/catapela/django-easy-contact',
      download_url='https://pypi.python.org/pypi/django-easy-contact',
      license='BSD',
      packages=find_packages(),
      include_package_data=True,
      keywords="django mail configuration setup mailform",
      classifiers=[
              'Development Status :: 4 - Beta',
              'Framework :: Django',
              'License :: OSI Approved :: BSD License',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Environment :: Console',
              'Natural Language :: English',
              'Natural Language :: German',
              'Intended Audience :: Developers',
              'Intended Audience :: Information Technology',
              'Topic :: Internet',
              'Topic :: Utilities',
              ],
      install_requires=REQUIRES,
      zip_safe=False,
      )
