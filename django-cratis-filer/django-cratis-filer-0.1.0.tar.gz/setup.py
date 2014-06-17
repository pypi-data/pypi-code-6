import os
from setuptools import setup, find_packages
# from tests import PyTest

setup(
    name='django-cratis-filer',
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
        'django-cms',
        'Pillow',
        'easy-thumbnails',
        'Pillow',
        'django-filer',
        'cmsplugin-filer'
    ]
)

