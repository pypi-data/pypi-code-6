from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

with open("README", "r") as fp:
    long_description = fp.read()

setup(name="require-python-3",
      version=1,
      author="Andrew Chase",
      author_email="theandychase@gmail.com",
      url="https://github.com/asperous/require-python-3",
      py_modules=["require_python_3"],
      description="Makes your script require python 3",
      long_description=long_description,
      license="MIT",
      classifiers=classifiers
      )
  