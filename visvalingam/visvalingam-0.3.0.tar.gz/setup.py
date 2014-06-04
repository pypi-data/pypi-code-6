#! /usr/bin/env python
# -*- coding:utf8 -*-

# Mathieu (matael) Gaborit <mathieu@matael.org> 2014

from setuptools import setup

setup(
    name='visvalingam',
    version='0.3.0',
    description='Simple implementation of the Visvalingam-Wyatt algorithm',
    author = 'Ralf Klammer',
    author_email = 'ralf.klammer@tu-dersden.de',
    maintainer='Mathieu (matael) Gaborit',
    maintainer_email='mathieu@matael.org',
    license='MIT',
    url='http://milkbread.github.io/Visvalingam-Wyatt',
    packages=['visvalingam', 'visvalingam.classes'],
    scripts=['bin/simplify.py'],
    classifiers=[
            'Programming Language :: Python',
            'Intended Audience :: Developers',
        ],
)

