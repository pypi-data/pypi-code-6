from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ZeoRawData',

    version='2.0',

    description='Zeo Raw Data Library',
    long_description=long_description,

    url='http://www.sleepstreamonline.com/rdl/',

    author='Brian Schiffer',
    author_email='brianschifferece@gmail.com',

    license='UNKNOWN',

    classifiers=[
        'Development Status :: 7 - Inactive',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: Other/Proprietary License',

        'Programming Language :: Python :: 2',
    ],

    keywords='zeo',

    packages=find_packages(),

    install_requires=['pyserial'],
)
