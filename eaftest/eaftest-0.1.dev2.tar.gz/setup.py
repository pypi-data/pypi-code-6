#!/usr/bin/env python

from setuptools import setup, Extension
import os

#libaft = Extension('libaft',
#                    sources = ['libaft/eaf2d.c', 'libaft/eaftest.c'])

# Compile libaft
os.system("make -C ./eaftest/libaft distclean libaft")

setup(
    name='eaftest',
    version='0.1.dev2',
    description=('Tools to perform hypothesis tests based on '
                 'the empirical attainment function.'),
    url='https://bitbucket.org/hjalves/eaftest',
    author='Humberto Alves',
    author_email='halves@uc.pt',
    license='GPL',
    classifiers=[
        'Development Status :: 1 - Planning',
        #'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
    keywords='eaf statistics opencl',
    packages=[
        'eaftest',
        'eaftest.utils',
        'eaftest.libaft',
        'eaftest.clkernels',
    ],
    package_data={
        'eaftest.libaft': ['libaft.so'],
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
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    zip_safe=False,
)