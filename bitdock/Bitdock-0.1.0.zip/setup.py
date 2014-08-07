# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import os
import re

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, 'source')
README_PATH = os.path.join(ROOT_PATH, 'README.rst')


# Read version from source.
with open(os.path.join(
    SOURCE_PATH, 'bitdock', '_version.py'
)) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        raise SystemExit(pytest.main(self.test_args))


setup(
    name='Bitdock',
    version=VERSION,
    description='Push Bitbucket pull requests to Flowdock.',
    long_description=open(README_PATH).read(),
    keywords='bitbucket, flowdock',
    url='https://bitbucket.org/ftrack/bitdock',
    author='ftrack',
    author_email='support@ftrack.com',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    setup_requires=[
        'sphinx >= 1.2.2, < 2'
    ],
    install_requires=[
        'cherrypy >= 3.2, <4',
        'requests >= 2.2, <3'
    ],
    tests_require=[
        'pytest >= 2.3.5, <3'
    ],
    cmdclass={
        'test': PyTest
    }
)
