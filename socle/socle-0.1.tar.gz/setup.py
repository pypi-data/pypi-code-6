#!/usr/bin/python
# coding: utf-8

from distutils.core import setup

setup(
    name='socle',
    author=u"Lauri Võsandi",
    author_email="lauri.vosandi@gmail.com",
    url="https://github.com/v6sa/socle",
    version='0.1',
    packages=['socle',],
    data_files=[
        ("", ["README.rst"])
    ],
    scripts = ["misc/socle"],
    license='MIT',
    long_description=open('README.rst').read(),
)
