#!/usr/bin/env python
"""
Install django-easyoptions using setuptools
"""

from easyoptions import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-easyoptions',
    version=__version__,
    description='Easily create extra Meta option classes on forms',
    author='Tim Heap',
    author_email='tim@timheap.me',
    url='https://bitbucket.org/tim_heap/django-easyoptions',

    install_requires=['Django>=1.4'],
    zip_safe=False,

    packages=find_packages(),

    include_package_data=True,
    package_data={ },

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
