#!/usr/bin/env python

from setuptools import setup

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
    name='django-creek',
    version='0.1.2',
    description='A simple flow controller for Django',
    author='Bo Lopker',
    author_email='blopker@23andme.com',
    url='https://github.com/23andMe/django-creek',
    keywords='django',
    packages=['django_creek'],
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ]
)
