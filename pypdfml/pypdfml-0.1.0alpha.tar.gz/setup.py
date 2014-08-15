# -*- coding: utf-8 -*-

__title__ = 'pypdfml'
__version__ = '0.1.0alpha'
__description__ = 'Simple XML wrapper for reportlab.'
__license__ = 'unknown'
__author__ = 'Manuel Badzong'
__author_email__ = 'manuel@andev.ch'

from setuptools import setup, find_packages

f = open('requirements.txt', 'r')
lines = f.readlines()
requirements = [l.strip().strip('\n') for l in lines if l.strip() and not l.strip().startswith('#')]
readme = open('README.md').read()

setup(name=__title__,
      version=__version__,
      description=__description__,
      author=__author__,
      author_email=__author_email__,
      url='https://github.com/badzong/pypdfml',
      packages=find_packages(),
      # zip_save=False,
      include_package_data=True,
      license=__license__,
      keywords='pdf generating reportlab report xml jinja',
      long_description=readme,
      install_requires=requirements,
)
