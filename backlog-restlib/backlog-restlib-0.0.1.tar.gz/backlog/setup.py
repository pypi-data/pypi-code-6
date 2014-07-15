# -*- coding: utf-8 -*-
from setuptools import setup
import os


os.chdir(os.path.normpath(
         os.path.join(os.path.join(os.path.abspath(__file__),
                      os.pardir), os.pardir)))

setup(name='backlog-restlib',
      version='0.0.1',
      description='''\
thin wrapper for Backlog API v2.
This is an experimental development''',
      author='kitsu yui',
      author_email='yui.kitsu+git@gmail.com',
      packages=['backlog'],
      install_requires=['requests==2.3.0']
      )
