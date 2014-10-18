import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
   return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="Fantasy_Basketball",
      version="0.1",
      author="Devin Kelly",
      author_email="dwwkelly@fastmail.fm",
      description=("A package that fetches, processes and visualizes " +
                   "fantasy basketball statistics"),
      license="GPL3",
      keywords = "fantasy basketball pandas",
      url = "https://github.com/dwwkelly/fantasy_basketball",
      test_suite="tests",
      scripts=['scripts/FB_Manager.py'],
      long_description=read('README.rst'),
      packages=find_packages(),
      include_package_data=True,
      install_requires=['Click', 'numpy', 'matplotlib',
                        'pandas', 'jinja2', 'pycurl',
                        'beautifulsoup4', 'lxml'],
      )
