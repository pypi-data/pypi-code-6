from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ops.py',
    description='Python Library for the Open PHACTS Platform API',
    version='0.1.0a1',
    packages=['ops', 'ops.test'],
    license='Apache 2.0',
    long_description=long_description,
    url='https://github.com/pgroth/ops.py',
    author='Paul Groth',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    keywords='api data integration, database, drug discovery',


)
