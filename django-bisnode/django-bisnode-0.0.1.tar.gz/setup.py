#!/usr/bin/env python

from setuptools import setup, find_packages
import bisnode

setup(
    name='django-bisnode',
    version=".".join(map(str, bisnode.__version__)),
    author='Rebecca Meritz',
    author_email='rebecca@fundedbyme.com',
    url='http://github.com/FundedByMe/django-bisnode',
    install_requires=[
        'Django>=1.4.15',
    ],
    description='Django package that helps in your Bisnode integration',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
