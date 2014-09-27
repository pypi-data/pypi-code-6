# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name = 'digitalocean-python',
    version = '0.1.4',
    packages = find_packages(),
    install_requires = ['requests'],
    author = 'Nashruddin Amin',
    author_email = 'nashruddin.amin@gmail.com',
    description = 'Python wrapper for the DigitalOcean API v2',
    license = 'MIT',
    keywords = 'digitalocean api python',
    url = 'https://github.com/bsdnoobz/pyocean'
)
