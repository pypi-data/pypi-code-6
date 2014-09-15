# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages


if sys.version_info < (3, 3):
    raise Exception('colibri requires Python 3.3 or higher')


# -*- Distribution Meta -*-
meta = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'colibri/_version.py')) as f:
    for line in f:
        key, value = line.split('=')
        meta[key.strip()] = value.strip("' \n")


with open('README.rst') as f:
    README = f.read()


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return [
        r for r in (
            strip_comments(l) for l in open(
                os.path.join(os.getcwd(), 'requirements', *f)).readlines()
        ) if r]


install_requires = reqs('default.txt')
if sys.version_info < (3, 4):
    install_requires.extend(reqs('py3.txt'))


setup(
    name='colibri',
    version=meta['__version__'],
    author=meta['__author__'],
    author_email=['__contact__'],
    description='asyncio-based implementation of AMQP client',
    long_description=README,
    keywords='colibri AMQP client asyncio',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url='http://pypi.python.org/pypi/colibri',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    include_package_data=False,
    zip_safe=False,
)
