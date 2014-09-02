#!/usr/bin/python

from setuptools import setup


setup(
    name='Zone',
    version='0.0.0dev',
    packages=['zone'],
    package_data={
        'zone': ['README.md'],
    },
    author='abing',
    author_email='',
    license='PRIVATE',
    description='Asynchronous RPC framework based on Apache Avro and Trollius',
    zip_safe=False,
    install_requires=[
        'avro==1.7.7',
        'futures==2.1.6',
        'kids==0.7.6',
        'trollius==1.0.1',
    ],
)

