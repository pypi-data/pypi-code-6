#!/usr/bin/env python

from distutils.core import setup

setup(name='copyipsum',
      version='0.0.1',
      description='Grab text from Loripsum.net API."',
      author='Jeremy Boggs',
      author_email='jeremy@clioweb.org',
      url='https://github.com/clioweb/copyipsum',
      scripts=['copyipsum'],
      install_requires=['requests']
     )

