#!/usr/bin/env python

from distutils.core import setup

setup(name='prorab',
      version='0.2.0.1',
      description='no description',
      author='Vasiliy Horbachenko',
      author_email='shadow.prince@ya.ru',
      url='',
      scripts=['prorab/bin/prorab', 'prorab/bin/prorabd', ],
      packages=['prorab', 'prorab.server', ],
     )
