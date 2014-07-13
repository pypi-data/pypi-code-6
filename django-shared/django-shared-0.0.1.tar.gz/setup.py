#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-shared',
    description='Additional Django functionality',
    version='0.0.1',
    author='Alexander Herrmann',
    author_email='darignac@gmail.com',
    license='MIT',
    url='https://github.com/dArignac/shared',
    packages=[
        'shared',
        'shared.management.commands',
        'shared.templatetags',
    ],
    long_description=open('README.rst').read(),
    install_requires=[
        'Django',
    ],
    dependency_links=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ]
)
