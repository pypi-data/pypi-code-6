"""
setup packaging script for TextShaper
"""

import os

version = "0.0"
dependencies = ['webob', 'which']

# allow use of setuptools/distribute or distutils
kw = {}
try:
    from setuptools import setup
    kw['entry_points'] = """
      [console_scripts]
      indent = textshaper.indent:main
      onelineit = textshaper.onelineit:main
      quote = textshaper.quote:main
      textshaper = textshaper.main:main
      url2txt = textshaper.url2txt:main
"""
    kw['install_requires'] = dependencies
except ImportError:
    from distutils.core import setup
    kw['requires'] = dependencies

try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.txt')).read()
except IOError:
    description = ''


setup(name='TextShaper',
      version=version,
      description="package to shape text blocks ",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://k0s.org/hg/TextShaper',
      license='MPL2',
      packages=['textshaper'],
      include_package_data=True,
      zip_safe=False,
      **kw
      )

