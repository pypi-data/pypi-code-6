#!/usr/bin/env python

from pip.req import parse_requirements
from setuptools import setup, find_packages


install_reqs = [str(ir.req) for ir in parse_requirements('requirements.txt')]
VERSION = open('VERSION').read()


setup(
  license='BSD',
  version=VERSION,
  name='tlpconfig',
  scripts=['tlpconfig'],
  author='Fernando Oliveira',
  package_dir={'tlpconfig': '.'},
  install_requires=list(install_reqs),
  author_email='fernando@fholiveira.com',
  long_description=open('README.md').read(),
  description='A GTK+ 3.10 app to configure TLP.',
  url = 'https://github.com/fholiveira/tlpconfig',
  keywords = ['battery', 'saving', 'energy', 'tlp', 'gtk'],
  download_url = 'https://github.com/fholiveira/tlpconfig/tarball/' + VERSION,
  packages=['tlpconfig', 
            'tlpconfig.tlp',
            'tlpconfig.tlp.models',
            'tlpconfig.tlp.views',
            'tlpconfig.tlp.views.categories',
            'tlpconfig.tlp.views.binders'],
  package_data={'tlpconfig': ['requirements.txt', 
                              'README.md',
                              'tlpconfig', 
                              'VERSION',
                              'data/help',
                              'data/*.json',
                              'data/ui/*.ui',
                              'data/ui/*.css',
                              'data/ui/categories/*.ui']},
  classifiers = ['License :: OSI Approved :: BSD License',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Intended Audience :: End Users/Desktop']
)
