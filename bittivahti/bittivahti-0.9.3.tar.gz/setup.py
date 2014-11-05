#!/usr/bin/env python
from setuptools import setup, find_packages
import os.path

# Read README for long description
BASE = os.path.dirname(__file__)
README = os.path.join(BASE, 'README.rst')
with open(README) as f:
    long_description = f.read()


setup(name='bittivahti',
      version='0.9.3',
      description="Bittivahti bandwidth monitor for Linux",
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet',
          'Topic :: System :: Networking',
          'Topic :: Utilities',
      ],
      keywords='',
      author='Joonas Kuorilehto',
      author_email='joneskoo@kapsi.fi',
      url='https://github.com/joneskoo/bittivahti',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      bittivahti=bittivahti.cli:main
      """
      )
