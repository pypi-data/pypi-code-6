from distutils.core import setup
setup(
  name = 'django_protoman',
  packages = ['django_protoman'], # this must be the same as the name above
  version = '0.1',
  description = 'Simple django app to help with prototyping',
  author = 'Scott Barkman',
  author_email = 'scottbarkman@gmail.com',
  url = 'https://github.com/ScottBarkman/django_protoman', # use the URL to the github repo
  download_url = 'https://github.com/ScottBarkman/django_protoman/tarball/{tag}', # I'll explain this in a second
  keywords = ['prototyping', 'prototype', 'helper'], # arbitrary keywords
  classifiers = [],

  install_requires=['django', ],

)
