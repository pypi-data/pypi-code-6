#!/usr/bin/env python
from setuptools import setup, find_packages


install_requires = [
    'djehuty==0.0.4',
]

setup(
    name='djehutyslack',
    version='0.0.4',
    description='chat bot service for djehuty',
    author='xica development team',
    author_email='info@xica.net',
    url='https://github.com/xica/djehutyslack',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    packages=find_packages(),
    install_requires=install_requires,
)
