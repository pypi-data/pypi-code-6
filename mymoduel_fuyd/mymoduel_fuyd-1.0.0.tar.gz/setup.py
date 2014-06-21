#!/usr/bin/python
#coding:utf8

__author__ = ['fuyadong']

from setuptools import setup, find_packages

setup(
    name='mymoduel_fuyd',
    version="1.0.0",
    url='http://www.osforce.cn',
    license='MIT',
    author='fuyadong',
    author_email='fuyadong2011@163.com',
    description='a distributed test framework',
    classifiers=[
        "Programming Language :: Python",
    ],
    platforms='any',
    keywords='framework nose testing',
    packages=find_packages(exclude=['test']),
    install_requires=[]
)