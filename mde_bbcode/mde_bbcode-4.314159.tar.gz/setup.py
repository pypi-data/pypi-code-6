#!/usr/bin/env python

from setuptools import setup

setup(name="mde_bbcode",
      version="4.314159",
      description="Klappfallscheibes BBCode Parser v4 auf Python 3 portiert",
      url="http://stuff.oorgle.de/bbcode/v4.html",
      maintainer="enkore",
      maintainer_email="public+mde_bbcode@enkore.de",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Programming Language :: Python :: 3",
      ],
      py_modules = ["bbcode", "bbcode_test"],
      )
