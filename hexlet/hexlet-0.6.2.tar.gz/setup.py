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
    version='0.6.2',
    description="CLI for hexlet.io",
    long_description=open('README.rst').read(),
    # packages=['towelstuff',],
    license='MIT',
    author="Kirill Mokevnin",
    author_email="mokevnin@gmail.com",
    url="http://hexlet.io",
    packages=find_packages(),
    tests_require=[
        "pytest",
        "clint",
        "pytest-cov",
        "responses",
    ],
    install_requires=[
        "pprintpp",
        'pyyaml==3.11',
        'requests==2.3.0',
        'python-i18n==0.3.0',
        'purl==0.8',
        'click==3.1'
    ],
    include_package_data=True,
    # # NOTE hack for tox
    package_data={
        'hexlet': data_files
        },
    entry_points={
        'console_scripts': [
            'hexlet=hexlet.cli:main',
            'hexlet-lesson=hexlet.lesson_cli:main'
            ],
    }
)
