#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '29.04.13 - 15:34'

from distutils.core import setup

setup(
    name='Tornado-Menumaker',
    version='0.1.1',
    author='Martin Martimeo',
    author_email='martin@martimeo.de',
    url='https://github.com/MartinMartimeo/tornado-menumaker',
    packages=['tornado_menumaker'],
    license='GNU AGPLv3+',
    platforms='any',
    description='simple tornado menus',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').readlines(),
    download_url='http://pypi.python.org/pypi/Tornado-Menumaker',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)