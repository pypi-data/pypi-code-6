#!/usr/bin/env python

from setuptools import setup, find_packages

from bdgt import get_version


setup(
    name="bdgt",
    version=get_version(),
    packages=find_packages(),

    install_requires=[
        'PyYAML==3.11',
        'SQLAlchemy==0.9.7',
        'asciitable==0.8.0',
        'beautifulsoup4==4.3.2',
        'colorama==0.3.2',
        'enum34==1.0',
        'mt940==0.1',
        'ofxparse==0.14',
        'parse-type==0.3.4',
        'parse==1.6.4',
        'six==1.8.0',
    ],

    scripts=[
        'bin/bdgt',
    ],

    package_data={
    },

    # Metadata for PyPI
    author="Jon Black",
    author_email="jon_black@mm.st",
    description="A command line budget application",
    long_description=open('README.md').read(),
    license="GPLv3",
    keywords="budget finance command-line console",
    url="https://github.com/jonblack/bdgt/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
    ],
)
