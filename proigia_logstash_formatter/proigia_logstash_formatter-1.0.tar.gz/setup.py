"""
Setup file for logstash_formatter as used by Proigia.

This setup file will install the logstash_formatter, as used by Proigia.
Is basically is a 'Patched' version of the python-logstash-formatter by
exoscale. [https://github.com/exoscale/python-logstash-formatter].
"""
import codecs
from os import path

import setuptools


def read(*parts):
    """Use the README.rst as general info."""
    return codecs.open(path.join(path.dirname(__file__), *parts),
                       encoding="utf-8").read()

setuptools.setup(
    name='proigia_logstash_formatter',
    version='1.0',
    description='JSON formatter meant for logstash',
    long_description=read('README.rst'),
    url='https://github.com/Proigia/proigia-logstash-formatter',
    author='Wouter van Bommel',
    author_email='wvanbommel@proigia.nl',
    license='MIT, see LICENSE file',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    zip_safe=False,
    install_requires=[
        'logstash-formatter>=0.5.7.1'
    ],
)
