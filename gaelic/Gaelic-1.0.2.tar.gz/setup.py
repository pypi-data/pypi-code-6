#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='Gaelic',
    version='1.0.2',
    description='Google App Engine package installer (pip bridge)',
    author='Jon Wayne Parrott',
    author_email='jjramone13@gmail.com',
    maintainer='Jon Parrott',
    maintainer_email='jjramone13@gmail.com',
    url='http://bitbucket.org/jonparrott/gaelic',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    py_modules=['gaelic'],
    install_requires=['distribute'],
    entry_points={
        'console_scripts': [
            'gaelic = gaelic:main'
        ]
    }
)
