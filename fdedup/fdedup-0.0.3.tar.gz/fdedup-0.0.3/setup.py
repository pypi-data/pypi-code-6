# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

setup(
    name='fdedup',
    packages=find_packages('fdedup', exclude=['static', 'tests', 'run_tests*',
                                              'requirements*']),
    version='0.0.3',
    description='File Deduplicator',
    author='Alexander Krasnukhin, Alexey Ulyanov',
    author_email='the.malkom@gmail.com, sibuser.nsk@gmail.com',
    url='https://github.com/themalkolm/fdedup',
    download_url='https://github.com/themalkolm/fdedup',
    keywords=['files', 'duplicates'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'
    ],
)
