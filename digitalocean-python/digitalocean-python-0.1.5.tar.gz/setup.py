# encoding: utf-8

from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError) as e:
    long_description = open('README.md').read()

setup(
    name = 'digitalocean-python',
    version = '0.1.5',
    packages = find_packages(),
    install_requires = ['requests'],
    author = 'Nashruddin Amin',
    author_email = 'nashruddin.amin@gmail.com',
    description = 'Python wrapper for the DigitalOcean API v2',
    long_description = long_description,
    license = 'MIT',
    keywords = 'digitalocean api python',
    url = 'https://github.com/bsdnoobz/pyocean'
)
