# coding=utf-8
from distutils.core import setup
setup(
  name = 'permalink_adder',
  version = '0.1.3',
  description = 'SEO tool for adding permalinks to text contained in Django apps databases.',
  author = u'Piotr Lizończyk',
  author_email = 'piotr.lizonczyk@gmail.com',
  url = 'https://github.com/plizonczyk/permalink_adder',
  download_url = 'https://github.com/plizonczyk/p`ermalink_adder/tarball/0.1',
  keywords = ['SEO', 'permalinks'],
  classifiers = ['Development Status :: 2 - Pre-Alpha',
                 'Framework :: Django',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7'],
  requires = ['django'],
  packages = ['permalink_adder',
              'permalink_adder.management',
              'permalink_adder.management.commands'],
)