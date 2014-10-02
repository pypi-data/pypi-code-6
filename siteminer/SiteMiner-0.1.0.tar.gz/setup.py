__author__ = 'massimo'

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "SiteMiner",
    version = "0.1.0",
    author = "massimo",
    author_email = "yangsibai@gmail.com",
    description = "crawl a site and find out all link http status code",
    license = "MIT",
    keywords = "http status site error",
    url = "https://github.com/yangsibai/SiteMiner",
    packages = ['Miner', "test"],
    long_description = read('README.md'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License"
    ]
)