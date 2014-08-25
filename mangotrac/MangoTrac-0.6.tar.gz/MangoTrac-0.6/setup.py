#!/usr/bin/env python

from setuptools import setup, find_packages

# requires = ['django', 'south', 'markdown']

setup(
      name             = 'MangoTrac',
      version          = '0.6',
      description      = 'Issue Tracker based on the Django admin app',
      author           = 'AK',
      author_email     = 'ak@lightbird.net',
      url              = 'https://github.com/akulakov/mangotrac',
      install_requires = ['django', 'south', 'markdown'],
      license          = "MIT",
      packages         = find_packages(),
      classifiers      = [
                     "Development Status :: 4 - Beta",
                     
                     "Framework :: Django",
                     "Intended Audience :: Developers",
                     "Intended Audience :: End Users/Desktop",
                     
                     "License :: OSI Approved :: MIT License",
                     
                     "Operating System :: POSIX :: Linux",
                     
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3.4",
                     
                     "Topic :: Software Development :: Bug Tracking",
                     ],
      long_description = """
      MangoTrac is an issue tracker based on the Django admin app. It's targeted at small and medium-sized
      teams and projects.

      Notable features are: ability to sort / filter by many columns like owner, status, priority, project,
      creator, etc; flexible reports with a easy to use tool to create them; small codebase -- easy to
      customize and tweak.
      """,
     )
