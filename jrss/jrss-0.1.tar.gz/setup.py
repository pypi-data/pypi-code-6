#coding: utf-8
from setuptools import setup

setup(
    version='0.1',
    name = "jrss",
    packages = ['jrss'],
    description='Torrent RSS downloader',
    author='Oskar Hallström',
    author_email='ooskar@ooskar.com',
    maintainer='Jakob Hedman',
    maintainer_email='jakob@hedman.email',
    license='GNU GPLv3',
    url='https://github.com/spillevink/jrss',
    package_dir = {'jrss':'jrss'},
    entry_points = {
        'console_scripts': [
            'jrss = jrss.jrss:main.command',
        ],
    },
    install_requires = [
        'opster',
        'configobj',
        'feedparser',
        'requests',
    ],
    long_description = open('README.rst').read(),
)
