#!/usr/bin/env python

PROJECT = 'occult'

VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Xcode Project Toolkit',
    long_description=long_description,

    author='Yulin Ding',
    author_email='sodabiscuit@gmail.com',

    url='https://github.com/sodabiscuit/occult',
    download_url='https://github.com/sodabiscuit/occult/tarball/master',

    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff',
                      'clint',
                      'jinja2',
                      'pillow',
                      'jsonschema',
                      ],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'occult = occult.main:main'
        ],
        'occult.manager': [
            'json = occult.json.cli:JSONUtility',
            'resource = occult.resource.cli:Resource',
            'error = occult.error:Error',
            'complete = cliff.complete.CompleteCommand',
        ],
    },

    zip_safe=False,
)