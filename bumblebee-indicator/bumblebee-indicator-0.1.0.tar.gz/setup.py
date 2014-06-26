#!/usr/bin/env python2

from setuptools import setup

setup(
  name         = 'bumblebee-indicator',
  version      = '0.1.0',
  description  = 'A Unity desktop bumblebee indicator - switch dual screens, enable 3d mode',
  url          = 'http://github.com/storborg/funniest',
  author       = 'Wave Software',
  author_email = 'info@wavesoftware.pl',
  license      = 'Apache License 2.0',
  packages     = ['bumblebee_indicator'],
  zip_safe     = True,
  scripts      = ['bin/bumblebee-indicator'],
  package_data = { 
    '': ['resources/*']
  }
)
