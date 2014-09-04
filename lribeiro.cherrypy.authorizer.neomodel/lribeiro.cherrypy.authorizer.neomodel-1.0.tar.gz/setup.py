from codecs import open
from os import path
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    
    def initialize_options(self):
        TestCommand.initialize_options(self)

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main('tests/')
        sys.exit(errno)


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lribeiro.cherrypy.authorizer.neomodel',
    version='1.0',
    description='Basic user model, authenticator and authorizer for cherrypy-authorizer and neomodel',
    long_description=long_description,
    url='http://bitbucket.org/livioribeiro/cherrypy-authorizer-neomodel',
    author='Livio Ribeiro',
    author_email='livioribeiro@outlook.com',
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: CherryPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ],
    keywords=['authentication', 'authorization', 'access control', 'cherrypy', 'neomodel'],
    packages=find_packages(exclude=['tests']),
    namespace_packages=['lribeiro', 'lribeiro.cherrypy', 'lribeiro.cherrypy.authorizer'],
    include_package_data=True,
    install_requires=[
        'CherryPy',
        'neomodel',
        'bcrypt',
        'lribeiro.cherrypy.authorizer'
    ],
    tests_require=[
        'pytest',
        'requests'
    ],
    cmdclass={'test': PyTest},
)