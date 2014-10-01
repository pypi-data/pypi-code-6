import os
import sys

from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

setup(
    name='ztilde',
    version='0.2',
    url='http://www.ztilde.com/',
    author='Thiago F Pappacena',
    author_email='pappacena@ztilde.com',
    description=('Python client lib for ztilde.com machine learning  services'),
    license='MIT',
    packages=find_packages(),
    install_requires=[

    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
