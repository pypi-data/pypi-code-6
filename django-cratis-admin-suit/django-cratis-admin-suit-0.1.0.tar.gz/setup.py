import os
from setuptools import setup, find_packages
# from tests import PyTest

setup(
    name='django-cratis-admin-suit',
    version='0.1.0',
    packages=find_packages(),

    url='',
    license='MIT',
    author='Alex Rudakov',
    author_email='ribozz@gmail.com',
    description='Integrates django-suit theme to django-admin',
    long_description='',
    install_requires=[
        'django-cratis',
        'setuptools',
        'django-suit'
    ]
)

