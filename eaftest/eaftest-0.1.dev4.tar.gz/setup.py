#!/usr/bin/env python

from setuptools import setup, Extension
import os, sys


# Compile C libraries
try:
    assert 0 == os.system("make -C ./eaftest/libaft")
    assert 0 == os.system("make -C ./eaftest/libeafbb lib")
except:
    print("Error building C libraries. Exiting...")
    sys.exit(1)

setup(
    name='eaftest',
    version='0.1.dev4',
    description=('Tools to perform hypothesis tests based on '
                 'the empirical attainment function.'),
    url='https://bitbucket.org/hjalves/eaftest',
    author='Humberto Alves',
    author_email='halves@uc.pt',
    license='GPL',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
    keywords='eaf statistics opencl',
    packages=[
        'eaftest',
        'eaftest.utils',
        'eaftest.libaft',
        'eaftest.libeafbb',
        'eaftest.clkernels',
    ],
    package_data={
        'eaftest.libaft': ['libaft.so'],
        'eaftest.libeafbb': ['libeafbb.so'],
        'eaftest.clkernels': ['*.cl'],
    },
    install_requires=[
        'numpy',
        'pyopencl',
    ],
    entry_points={
        'console_scripts': [
            'eaftest=eaftest.cmd:main',
        ],
    },
    #ext_modules=[libaft],
    #test_suite='nose.collector',
    #tests_require=['nose'],
    include_package_data=True,
    zip_safe=False,
)