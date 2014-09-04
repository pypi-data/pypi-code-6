#!/usr/bin/env python
"""
Install django-elasticfilter using setuptools
"""

from elasticfilter import __version__

with open('README.rst', 'r') as f:
    readme = f.read()

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-elasticfilter',
    version=__version__,
    description=('Create forms that run Elasticsearch queries'),
    long_description=readme,
    author='Tim Heap',
    author_email='tim@timheap.me',
    url='https://bitbucket.org/tim_heap/django-elasticfilter/',

    install_requires=[
        'Django>=1.6',
        'elasticutils>=0.10',
    ],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(),

    include_package_data=True,
    package_data={ },

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
