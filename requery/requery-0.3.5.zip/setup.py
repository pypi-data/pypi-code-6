# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='requery',
    version='0.3.5',
    url='http://github.com/ebertti/requery/',
    author='Ezequiel Bertti',
    author_email='ebertti@gmail.com',
    install_requires=['django>=1.7', 'Pygments>=1.6'],
    packages=['requery'],
    include_package_data=True,
    license='MIT License',
    platforms=['OS Independent'],
    description="Simple way to store and use querys in database for use of DBA's for Django Admin",
    long_description=(open('README.rst').read()),
    keywords='query dba repository report django',
    zip_safe=False,
)
