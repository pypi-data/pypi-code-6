# -*- coding: utf-8 -*-
from setuptools import setup
import os
import sys


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name='drax',
    version='0.4.0',
    author='tax',
    author_email='paultax@gmail.com',
    include_package_data=True,
    description='Drax is a react and python implementation of the dashing'
                'dashboard',
    long_description=open('README.md').read(),
    url='http://github.com/tax/drax',
    license='MIT',
    packages=['drax'],
    entry_points={
        'console_scripts': ['drax=drax.commands:main'],
    },
    install_requires=[
        'tornado>=4.0.2',
    ],
    zip_safe=False)
