#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of thumbor-web.
# https://github.com/thumbor/thumbor-web

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Bernardo Heynemann heynemann@gmail.com


from setuptools import setup, find_packages
from thumbor_web import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
    'thumbor',
    'honcho',
    'Sphinx==1.2.3',
    'sphinx_rtd_theme',
    'thumbor==4.4.1',
]

setup(
    name='thumbor-web',
    version=__version__,
    description='thumbor website',
    long_description='''
thumbor website
''',
    keywords='thumbor web',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='https://github.com/thumbor/thumbor-web',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        "Programming Language :: Python :: 2.7",
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'derpconf==0.7.2',
        'flask',
        'flask-assets',
        'alembic',
        'mysql-python',
        'Flask-SQLAlchemy',
        'webassets',
        'flask-debugtoolbar',
        'ujson',
        'jsmin',
        'cssmin',
        'libthumbor',
        'markdown',
        'Flask-Login',
        'Flask-Admin',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            'thumbor-web=thumbor_web.run:main',
        ],
    },
)
