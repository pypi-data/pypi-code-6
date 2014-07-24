#!/usr/bin/env python

from setuptools import setup
import re


def get_version():
    with open('icanhasfile.py') as file:
        version_file = file.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                  version_file, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


def get_long_description():
    with open('README.rst') as readme:
        # skip text before the 'pypi-split' string since the pypi site
        # renders that content from the name and description fields
        return readme.read().strip().split('.. comment: pypi-split', 1)[1]


setup(
    name='icanhasfile',
    version=get_version(),
    description='COMPUTR, U HAS FILE. I CAN HAS IT?',
    long_description=get_long_description(),
    author='Arthur Loder',
    author_email='art@artloder.com',
    url='http://www.artloder.com/code/icanhasfile/',
    license='MIT',
    include_package_data=True,
    py_modules=['icanhasfile'],
    install_requires=['docopt'],
    entry_points={
        'console_scripts': ['icanhasfile = icanhasfile:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ]
)
