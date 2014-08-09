"""
Flask-Manifest
-------------

Asset manifest integration with Flask.
"""
import codecs
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


def read(filename):
    return codecs.open(filename, 'r', encoding='utf-8').read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='Flask-Manifest',
    version='0.2.0',
    url='https://github.com/ryankask/flask-manifest',
    license='BSD',
    author='Ryan Kaskel',
    author_email='dev@ryankaskel.com',
    description='Asset manifest integration with Flask.',
    long_description=read('README.rst'),
    py_modules=['flask_manifest'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask'],
    tests_require=['pytest', 'pytest-cov', 'mock'],
    cmdclass={
        'test': PyTest
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
