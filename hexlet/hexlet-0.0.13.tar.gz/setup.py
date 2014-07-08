from setuptools import setup, find_packages
import os
from os import path

data_files = [path.join(dp.split(os.sep, 1)[1], f)
        for dp, dn, filenames in os.walk("hexlet/data")
        for f in filenames
        if f[0] != '.']

# raise Exception(data_files)

setup(
    name='hexlet',
    version='0.0.13',
    description="CLI for hexlet.io",
    long_description=open('README.rst').read(),
    # packages=['towelstuff',],
    license='MIT',
    author="Kirill Mokevnin",
    author_email="mokevnin@gmail.com",
    url="http://hexlet.io",
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'requests',
        'python-i18n==0.3.0',
        'click==2.4',
        'purl'
    ],
    # NOTE hack for tox
    package_data = {
        'hexlet': data_files
        },
    entry_points = {
        'console_scripts': [
            # 'hexlet=hexlet.cli:main',
            'hexlet-lesson=hexlet.lesson_cli:main'
            ],
    }
)
