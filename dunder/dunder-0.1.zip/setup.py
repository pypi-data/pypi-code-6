# Copyright 2009-2014, Simon Kennedy, sffjunkie+code@gmail.com

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(name='dunder',
      version='0.1',
      description='Extract dunder variables from a Python source file.',
      long_description="""Provides a `parse` function to extract all the
      dunder variables e.g. __version__ from a Python source file.
      """,
      author='Simon Kennedy',
      author_email='sffjunkie+code@gmail.com',
      url="https://launchpad.net/dunder.py",
      license='Apache-2.0',
      package_dir={'': 'src'},
      py_modules=['dunder'],

      tests_require=['tox'],
      cmdclass={'test': Tox},
)
