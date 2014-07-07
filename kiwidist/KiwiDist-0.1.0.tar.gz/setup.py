# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='KiwiDist',
    version='0.1.0',
    author='F. Gatto and L. Väremo',
    author_email=['kiwi@sysbio.se'],
    packages=['kiwi'],
    url='http://sysbio.se/kiwi/',
    license='LICENSE.txt',
    description='Combining gene-set analysis with network properties.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.8.0",
        "matplotlib >= 1.3.1",
        "networkx >= 1.8.1",
        "mygene >= 2.1.0",
        ],
)