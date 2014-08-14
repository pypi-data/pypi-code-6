# coding=utf-8
from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

setup(
  name = 'internal_links',
  version = '0.1.4.6',
  description = 'SEO tool for adding links to text contained in Django apps databases.',
  author = u'Piotr Lizończyk',
  author_email = 'piotr.lizonczyk@gmail.com',
  url = 'https://github.com/deployed/internal_links',
  download_url = 'https://github.com/deployed/internal_links/tarball/0.1.4.6',
  keywords = ['SEO'],
  classifiers = ['Development Status :: 2 - Pre-Alpha',
                 'Framework :: Django',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7'],
  requires = ['django'],
  packages = ['internal_links',
              'internal_links.management',
              'internal_links.management.commands'],
  long_description = long_description,
  obsoletes=['permalink_adder']
)
