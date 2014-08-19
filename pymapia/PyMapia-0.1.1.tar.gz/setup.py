# coding=utf-8
from setuptools import setup
from os import path

from pymapia import __version__

base_dir = path.abspath(path.dirname(__file__))

setup(
    name='PyMapia',
    version=__version__,
    description='Python SDK for WikiMapia (http://wikimapia.org)',
    url='https://github.com/boisei0/pymapia',
    author='Rob Derksen',
    author_email='rob.derksen@hubsec.eu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='sdk api maps wiki',
    install_requires=['requests'],
    packages=['pymapia']
)