import os
from setuptools import setup, find_packages
# from tests import PyTest

setup(
    name='django-cratis-cms',
    version='0.1.0',
    packages=find_packages(),

    url='',
    license='MIT',
    author='Alex Rudakov',
    author_email='ribozz@gmail.com',
    description='Integrates django-cms into cratis application',
    long_description='',
    install_requires=[
        'django-cratis',
        'setuptools',
        'django-mptt==0.5.2',
        'django-cms',
        'Pillow',
    ],

    dependency_links=[
        'git://github.com/ribozz/django-cms.git@aa43b1715bdb39ac507d4ffac53e7c6bf7998e48#egg=django-cms'
    ]
)

