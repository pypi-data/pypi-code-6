from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='jbcnfw',
      version=version,
      author='Neal Williams',
      author_email='nealfwilliams@gmail.com',
      description="Resource traversal app",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "zeo", # On PyPI
        "zodb", # An Affle package
      ],
      )

