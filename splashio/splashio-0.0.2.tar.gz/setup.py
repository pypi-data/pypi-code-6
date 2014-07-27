
__author__='''
Dawson Reid (dawson@streamlyne.co)
'''


from setuptools import setup, find_packages, Command

def parse_packages(package_file, packages=[]):
    with open(package_file, 'r') as f:
        for line in f:
            packages.append(line.rstrip())
    return packages

install_packages = parse_packages('require/common.txt')


import os, sys, subprocess
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
  '''
  '''
  user_options = []

  def finalize_options(self):
      TestCommand.finalize_options(self)
      self.test_args = []
      self.test_suite = True

  def run_tests(self):

    # bootstrap the python path
    dirname = os.getcwd()
    sys.path.insert(0, os.path.join(dirname, 'splash'))
    #sys.path.insert(0, os.path.join(dirname, 'tests'))

    import pytest
    errno = pytest.main(self.test_args)

    sys.exit(errno)


setup(name='splashio',
  version='0.0.2',
  description="The splash SDK server.",
  packages=find_packages(),
  install_requires=install_packages,
  tests_require=['pytest'],
  cmdclass={
    'test': PyTest
  },

  url='https://github.com/Splash-io',
  download_url='https://github.com/Splash-io/splash-python/archive/0.0.2.tar.gz',
  keywords=['splash', 'sdk', 'event'],

  author='Dawson Reid',
  author_emial='dreid93@gmail.com',
  maintainer='Dawson Reid',
  maintainer_email='dreid93@gmail.com'
)
