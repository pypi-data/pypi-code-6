#! /usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup
import os.path

setup(name='simplehttpmonitor',
      version='1.0.0',
      description='simplehttpmonitor',
      author='Nicolas Vanhoren',
      author_email='nicolas.vanhoren@unknown.com',
      url='https://github.com/nicolas-van/simplehttpmonitor',
      py_modules = [],
      packages=[],
      scripts=["simplehttpmonitor"],
      long_description='Monitors a web server. This program is meant to be called by cron and' +
        " will send a mail to an administrator to report a problem.",
      keywords="",
      license="MIT",
      classifiers=[
          ],
      install_requires=[
        "argparse",
        "requests",
        ],
     )

