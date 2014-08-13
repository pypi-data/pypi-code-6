#!/usr/bin/env python
#encoding:utf-8
from setuptools import setup,find_packages

setup(
    name = 'maxxn',
    author = 'seraph0017',
    author_email = 'seraph0017@hotmail.com',
    version = '1.0.0',
    description = 'simple crawler',
    keywords = 'simple crawler',
    packages = find_packages(),
    package_data = {
        'maxxn':['*.*','maxxn/*.*']
        },
    install_requires = [
            'requests','BeautifulSoup4'
            ],
    platforms = 'any',
    entry_points = """
        [console_scripts]
        maxxn = maxxn:main
    """
        )
