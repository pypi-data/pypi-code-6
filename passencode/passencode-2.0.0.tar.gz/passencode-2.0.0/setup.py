#! /usr/bin/python
from setuptools import setup
import os.path

setup(name='passencode',
      version='2.0.0',
      description='passencode',
      author='Nicolas Vanhoren',
      author_email='nicolas.vanhoren@unknown.com',
      url='https://github.com/nicolas-van/passencodeu',
      py_modules = [],
      packages=[],
      scripts=["passencode"],
      long_description="Simple program to generate a password hash using passlib",
      keywords="",
      license="MIT",
      classifiers=[
          ],
      install_requires=[
        "passlib",
        "click >= 3.3",
        ],
     )

