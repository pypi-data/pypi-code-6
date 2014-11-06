#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='coursera-downloader',
    version='0.2',
    url='https://github.com/huanghao/coursera-downloader',
    author='Huang, Hao',
    author_email='huang1hao@gmail.com',
    packages=find_packages(),
    scripts=[
        'coursera-dl.py',
    ],
    install_requires=[
        'pyquery',
        'selenium',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        ],
    )
