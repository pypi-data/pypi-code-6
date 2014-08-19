# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst', 'rt') as f:
    long_description = f.read()

setup(
    name='pymoji',
    version='0.1.0',
    description='Converter between Emoji Unicode and Ascii Text.',
    author='mapix',
    author_email='mapix.me@gmail.com',
    url='https://github.com/mapix/pymoji',
    license='MIT',
    packages=find_packages(),
    install_requires=['distribute',],
    long_description=long_description,
)
