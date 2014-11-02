#!/usr/bin/env python
from distutils.core import setup

with open('README.txt') as fobj:
    README = fobj.read()

setup(name="funsizer",
      version="0.1",
      author="Mihai Tabara",
      author_email="tabara.mihai@gmail.com",
      maintainer="Mihai Tabara",
      maintainer_email="tabara.mihai@gmail.com",
      url="https://github.com/MihaiTabara/funsizer",
      description="Command line client to retrieve partials from https://github.com/mozilla/build-funsize",
      long_description=README,
      license="MPL",
      scripts=["funsizer.py"],
      classifiers=[],
      install_requires=[
          'requests==2.2.1',
      ],
      )
