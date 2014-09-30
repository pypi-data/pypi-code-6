#!/usr/bin/env python

import os
import setuptools

import version_info


def read_from_root(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Version Control',
]


setuptools.setup(
    author='Piotr Kilczuk',
    author_email='piotr@tymaszweb.pl',
    name='python-version-info',
    version='.'.join(str(v) for v in version_info.VERSION),
    description='Easy way to find out and display VCS versions of your projects',
    long_description=read_from_root('README.rst'),
    url='https://github.com/TyMaszWeb/python-version-info',
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=read_from_root('requirements.txt').split(),
    tests_require=read_from_root('test-requirements.txt').split(),
    packages=setuptools.find_packages(),
    include_package_data=False,
    # test_suite='runtests.main',
)
