# encoding: utf-8

from __future__ import absolute_import, print_function

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


__version__ = '0.2.8'
__author__ = 'Dmitry Orlov <me@mosquito.su>'


setup(name='postboy',
    version=__version__,
    author=__author__,
    author_email='me@mosquito.su',
    license="MIT",
    description="simple distributed emailing system.",
    platforms="all",
    url="http://github.com/mosquito/postboy",
    classifiers=[
      'Environment :: Console',
      'Programming Language :: Python',
    ],
    long_description=open('README.md').read(),
    packages=[
      'postboy',
    ],
    scripts=['bin/postboy-broker', 'bin/postboy-worker'],
    install_requires=[
        'pyzmq'
    ],
    requires=[
        'pyzmq'
    ],
)
