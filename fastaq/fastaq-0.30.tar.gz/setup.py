#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

sys.path.insert(0,'fastAQ')

sys.path.pop(0)

packages = ['fastAQ',
            'fastAQ.commandLineTools']

setup(
    name='fastaq',
    version='0.30',
    author='Janu Verma',
    author_email='jv367@cornell.edu',
    description='fastAQ is a very and super lightweight package for working with FASTA/FASTQ sequences',
    url='https://github.com/Jverma/fastAQ',
    platforms=['Linux','Mac OSX', 'Windows', 'Unix'],
    keywords=['Genomics','Quantitative genetics', 'python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        #'License ::MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=packages,
    #package_data={'TextGraphics':['Data/*.txt']},
    license='MIT'
    )			