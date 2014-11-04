#!/bin/env python
# -*- coding: utf8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = "0.1.0"

setup(
    name="buzzer_as_a_service.message",
    version=version,
    description="A test message plugin for BaaS",
    classifiers=[],
    keywords="",
    author="Liam Middlebrook",
    author_email="liammiddlebrook@gmail.com",
    url="https://github.com/liam-middlebrook/baas-message",
    license="MIT",
    scripts=[
        "distribute_setup.py",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "",
    ],
    py_modules=['buzzer_as_a_service.message'],
)
