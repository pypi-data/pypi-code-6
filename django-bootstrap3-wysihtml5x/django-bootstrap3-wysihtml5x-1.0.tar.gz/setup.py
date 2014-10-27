#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test

def run_tests(*args):
    from bootstrap3_wysihtml5x.tests import run_tests
    run_tests()

test.run_tests = run_tests

setup(
    name = "django-bootstrap3-wysihtml5x",
    version = "1.0",
    packages = find_packages(),
    include_package_data = True,
    license = "MIT",
    description = "Simple Django app that provides a Wysihtml5x rich-text editor widget.",
    long_description = "Simple Django app that provides a Wysihtml5x widget. Wysihtml5x is an active fork of the popular Wysihtml5 reach-text editor, supported by the original authors (XING). Originally fork from http://github.com/danirus/django-wysihtml5 by Daniel Rus Morales <http://danir.us/>",
    author = "Cédric Foellmi",
    author_email = "cedric@onekilopars.ec",
    maintainer = "Cédric Foellmi",
    maintainer_email = "cedric@onekilopars.ec",
    url = "http://pypi.python.org/pypi/django-bootstrap3-wysihtml5x/",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    test_suite = "bootstrap3_wysihtml5x",
)
