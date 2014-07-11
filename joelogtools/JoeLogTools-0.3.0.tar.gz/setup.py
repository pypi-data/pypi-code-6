# Name: setup.py
# Author: Joseph Gordon
# Date Created: Thursday July 10, 2014

import sys
from setuptools import setup, find_packages

setup(
    name='JoeLogTools',
    version='0.3.0',
    author='Joseph Gordon',
    author_email='j.gordon.matthew@gmail.com',
    packages=['joelogtools'],
    url='https://bitbucket.org/jmg099120/joelogtools',
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
)
