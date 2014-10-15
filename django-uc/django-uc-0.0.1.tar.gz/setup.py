#!/usr/bin/env python

from setuptools import setup, find_packages
import uc

setup(
    name='django-uc',
    version=".".join(map(str, uc.__version__)),
    author='Rebecca Meritz',
    author_email='rebecca@fundedbyme.com',
    url='http://github.com/FundedByMe/django-uc',
    install_requires=[
        'Django>=1.4.15',
    ],
    description='Django package that helps in your UC integration',
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
