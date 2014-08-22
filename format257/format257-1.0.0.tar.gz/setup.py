from setuptools import setup

from os import path

here = path.dirname(__file__)

with open(path.join(here, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setup(
    name='format257',
    version='1.0.0',
    description='Format docstrings as per PEP 257',
    long_description=long_description,


    author='Barret Rennie',
    author_email='barret@brennie.ca',
    url='https://github.com/brennie/format257',

    license='Public Domain',

    classifiers=[
        'Development Status :: 7 - Inactive',
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],

    packages=['format257'])
