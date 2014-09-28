# Setup script for PyDitz.

from conf.ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

try:
    from hgtools.managers import MercurialManager
    version = MercurialManager().get_current_version(increment='0.1')
    print "version", version
    with open("ditz/version.py", "w") as fp:
        fp.write("'%s'\n" % version)
except ImportError:
    pass


import ditz
import ditz.pkginfo as info
from ditz.config import config


setup(name             = info.__title__,
      author           = info.__author__,
      author_email     = info.__email__,
      description      = ditz.__doc__.strip(),
      long_description = open("README").read(),
      license          = info.__license__,
      url              = info.__url__,
      classifiers      = info.__classifiers__.strip().split("\n"),

      packages = ["ditz"],
      include_package_data = True,
      use_vcs_version = {'increment': '0.1'},

      setup_requires = [
          'hgtools',
          'flake8',
      ],

      install_requires = [
          'pyyaml >= 3.10',
          'jinja2 >= 2.7',
      ],

      tests_require = [
          'nose >= 1.3.0',
          'coverage >= 3.6',
          'mock >= 1.0.1',
      ],

      test_suite = 'nose.collector',

      entry_points = {
          'console_scripts': [
              '%s = ditz.console:main' % config.get('config', 'command')
          ]
      })

# flake8: noqa
