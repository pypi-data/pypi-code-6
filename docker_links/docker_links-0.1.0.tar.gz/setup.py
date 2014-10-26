#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='docker_links',
    version='0.1.0',
    description='Parse Docker links into values useful for Django settings.',
    long_description=readme + '\n\n' + history,
    author='Kit La Touche',
    author_email='kit@transneptune.net',
    url='https://github.com/wlonk/docker_links',
    packages=[
        'docker_links',
    ],
    package_dir={'docker_links':
                 'docker_links'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='docker_links',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
