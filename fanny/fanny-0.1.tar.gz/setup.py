#!/usr/bin/env python 

"""New project"""

from setuptools import find_packages, setup

setup(name = 'fanny',
      version = '0.1',
      description = "Factorial module.",
      long_description = "A test module for our book.",
      platforms = ["Linux"],
      author = "Kushal Das",
      author_email = "kushaldas@gmail.com",
      url = "http://pymbook.readthedocs.org/en/latest/",
      license = "MIT",
      packages = find_packages()
     )


