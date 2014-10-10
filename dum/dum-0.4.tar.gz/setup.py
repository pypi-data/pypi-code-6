# coding:utf8

from setuptools import setup, find_packages # Always prefer setuptools over distutils
from codecs import open # To use a consistent encoding
from os import path
here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'doc', 'intro.rst'), encoding='utf-8') as f:
    long_description = f.read()



setup(
    name='dum',
    version='0.4',
    description='Direct data to object for xml, jon and csv',
    long_description=long_description,
    # The project's main homepage.
    url='https://bitbucket.org/sebkeim/dum',
    # Author details
    author='Sébastien Keim',
    author_email='s.keim@free.fr',
    # Choose your license
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='xml csv json',
    py_modules = ["dum", "dumxpath"],
    test_suite="tests",
)
