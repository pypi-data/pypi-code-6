#!/usr/bin/env python

from setuptools import setup, find_packages
from lazy_admin import VERSION

setup(
    name='django_lazy_admin',
    version=VERSION,
    description='Enhancement for custom columns in django admin list screens',
    long_description=open('README.md').read(),
    author='Gautam Kachru',
    author_email='gautam@live.in',
    url='https://github.com/gkachru/django_lazy_admin',
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['django'],
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)