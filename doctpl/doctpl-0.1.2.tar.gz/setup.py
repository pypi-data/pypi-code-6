#!/usr/bin/env python

from setuptools import setup

setup(
    name='doctpl',
    version='0.1.2',
    author='Zhan Haoxun',
    author_email='programmer.zhx@gmail.com',
    url='https://github.com/haoxun/DocTemplate',
    license='MIT',
    description=('CLI tool for quickly setting '
                 'up templates for writing articles.'),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],

    install_requires=['docopt==0.6.1'],
    packages=['doctpl'],
    entry_points={
        'console_scripts': [
            'doctpl = doctpl.interface:main',
        ],
    },
    test_suite='tests.load_tests',
)
