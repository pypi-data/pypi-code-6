import sys
import os
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with codecs.open('README.rst', encoding='utf-8') as f:
    README = f.read()

with codecs.open('CHANGELOG.rst', encoding='utf-8') as f:
    CHANGELOG = f.read()

setup(
    name='check_puppetdb_node',
    version='0.0.1',
    author='Daniele Sluijters',
    author_email='daniele.sluijters+pypi@gmail.com',
    py_modules=['check_puppetdb_node'],
    url='https://github.com/daenney/check_puppetdb_node',
    license='Apache License 2.0',
    description='Nagios plugin to check Puppet run status through PuppetDB',
    long_description='\n'.join((README, CHANGELOG)),
    keywords='puppet puppetdb nagios agent run status',
    tests_require=['pytest', 'pytest-pep8'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': ['check_puppetdb_node=check_puppetdb_node:main'],
        },
    install_requires=[
        "pypuppetdb >= 0.1.1",
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Monitoring'
        ],
    )
