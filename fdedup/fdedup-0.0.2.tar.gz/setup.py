# -*- coding: utf-8 -*-

import re


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


from distutils.core import setup

setup(
    name='fdedup',
    packages=['fdedup'],  # this must be the same as the name above
    version=get_version('fdedup/__init__.py'),
    description='File Deduplicator',
    author='Alexandr Krasnukhin, Alexey Ulyanov',
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
