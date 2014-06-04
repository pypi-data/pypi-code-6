import os
import sys

from setuptools import find_packages
from setuptools import setup

setup(
    name='okapi',
    version='0.4',
    author='RedBeacon',
    author_email='support@redbeacon.com',
    description='Python Library to send API info to Storage Server',
    packages=find_packages(),
    data_files=[('config',['setup.cfg'])],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    install_requires = [
        'pymongo',
        'mongo',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'okapi=okapi:mongo',
        ],
    },
)