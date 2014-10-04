# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
sys.path.insert(0, '.')
version = __import__('tornform').__version__

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    print('WARNING: Could not locate pandoc, using Markdown long_description.')
    long_description = open('README.md').read()

description = long_description.splitlines()[0].strip()


setup(
    name='tornform',
    url='http://github.com/likang/tornform',
    download_url='http://pypi.python.org/pypi/tornform',
    version=version,
    description=description,
    long_description=long_description,
    license='MIT',
    platforms=['any'],
    py_modules=['tornform'],
    author='Kang Li',
    author_email='i@likang.me',
    install_requires=[
        'setuptools >= 0.6b1',
        'voluptuous',
    ],
)
