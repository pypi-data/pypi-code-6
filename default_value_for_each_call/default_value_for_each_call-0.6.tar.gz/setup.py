#!/usr/bin/env python
# coding=utf-8
__author__ = 'chenfengyuan'

from setuptools import setup

setup(
    name="default_value_for_each_call",
    version="0.6",
    author="Chen Fengyuan",
    author_email="jeova.sanctus.unus@gmail.com",
    description="compute function default value for each call",
    license="BSD",
    keywords="example documentation tutorial",
    py_modules=['default_value_for_each_call'],
    long_description="""Return a function whose default values will be computed for each call,
    instead of evaluating the default values when function definition is executed.

    make sure this function is the last(closest to the function) decorator
    Usage:
    @default_value_for_each_call.compute_default_value_for_each_call
    def foo(a=([])):
        a.append(3)
        print a

    foo()
    foo()

    Output:
    [3]
    [3]"""
)
