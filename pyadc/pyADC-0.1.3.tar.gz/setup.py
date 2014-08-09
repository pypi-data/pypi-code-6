#!/usr/bin/python
from distutils.core import setup

setup(
    name='pyADC',
    version='0.1.3',
    author='Brian Sykes',
    author_email='bsykes@bdscomputers.com',
    packages=['pyadc'],
    url='http://pypi.python.org/pypi/pyADC/',
    license='LICENSE.txt',
    description='Python implementation of the ADC(S) Protocol for Direct Connect.',
    long_description=open('README.txt').read(),
    install_requires=[
        "python-mhash >= 1.4",
        "tiger >= 0.3",
        "enum34 >= 1.0"
    ],
)

