import os
from setuptools import setup, find_packages
version = '0.1.3'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read() + '\n'
setup(name='darksky_catalog',
      version=version,
      description=("Catalog of Dark Sky Simulations"),
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          ("Topic :: Software Development :: Libraries :: Python Modules"),
      ],
      keywords='data',
      author='Matthew Turk <matthewturk@gmail.com>, Samuel Skillman <samskillman@gmail.com>, Michael S. Warren <mswarren@gmail.com>',
      license='BSD',
      packages=find_packages(),
      install_requires = ['yt','thingking'],
      )
