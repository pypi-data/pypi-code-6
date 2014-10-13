# coding: utf-8
#

from setuptools import setup, find_packages

long_description = ''
try:
    with open('README.md') as f:
        long_description = f.read()
except:
    pass

setup(
      name='gcfg',
      version='0.1',
      description='convert *.ini to python Model for easy access',
      long_description=long_description,

      author='codeskyblue',
      author_email='codeskyblue@gmail.com',

      packages = find_packages(),
      include_package_data=True,
      package_data={},
      install_requires=[],
      )
