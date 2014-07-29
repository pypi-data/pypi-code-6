#!/usr/bin/env python3

from setuptools import setup, find_packages
""" This file is used to build the 'NetAna' distrubtion.
    All files in 'examples' directory and all files defined in the MANFEST.in
    template file. """
setup(name='netana',
      version = '3.0.1',
      install_requires=['python>=3.4','python3-matplotlib>=1.3'],
      zip_safe=True,
      scripts = ["cp-examples.sh"],
      packages=['netana'],
      package_data={'netana': ['examples/*', 'doc/*']},
      author= 'James Bainter',
      maintainer= 'James Bainter',
      author_email= 'support@netana.org',
      description= 'Electronic Network Analyzer',
      long_description= 'This program solves electronic AC & DC Mash and Node network equations using matrix algebra.',
      platforms= [ 'Linux', 'MSWindows' ],
      keywords="network circuit node mash analysis",
      license = "GPL-3 - GNU General Public License",
      url = 'http://www.netana.org'
      )

