import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='django-keen',
    version='0.1.2',
    author='Jannis Gebauer',
    author_email='',
    packages=['dkeen',],
    url='http://pypi.python.org/pypi/django-keen/',
    license='LICENSE.txt',
    description='Simple wrapper for django around the official keen.io client',
    long_description=open('README.md').read(),
    install_requires=required
)