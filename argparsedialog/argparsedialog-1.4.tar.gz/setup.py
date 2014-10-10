#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='argparsedialog',
    version='1.4',
    packages=['argparsedialog/'],

    install_requires=[line.strip() for line in open('requirements.txt').readlines()],

    url='https://github.com/horejsek/python-argparsedialog',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    description='Python library converting argparse to Wizzard using dialog.',
    license='PSF',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: Unix',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
