#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'six>=1.8.0,<2.0.0',
    'PyCrypto>=2.6.1,<2.7.0'
]

test_requirements = [
]

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    test_requirements.append('unittest2')

if (
    sys.version_info[0] == 2 and sys.version_info[1] < 7 and
    sys.version_info[0] == 3 and sys.version_info[1] < 2
):
    requirements.append('argparse')

setup(
    name='pcf_decrypt',
    version='0.1.1',
    description='Decrypt encoded passwords in Cisco VPN pcf files.',
    long_description=readme + '\n\n' + history,
    author='Joachim Brandon LeBlanc',
    author_email='demosdemon@gmail.com',
    url='https://github.com/demosdemon/pcf_decrypt',
    packages=[
        'pcf_decrypt',
    ],
    package_dir={'pcf_decrypt': 'pcf_decrypt'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pcf_decrypt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'pcf_decrypt = pcf_decrypt.__main__:main'
        ],
    },
)
