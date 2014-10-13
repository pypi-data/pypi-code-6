from setuptools import setup, find_packages

version = '0.2.1'

setup(
    name='cmsplugin-plaintext-djangocms3',
    version=version,
    description='Adds a plaintext plugin for django-cms. Forked from https://bitbucket.org/xenofox/cmsplugin-plaintext to add django-cms3 support',
    author='Changer',
    author_email='support@changer.nl',
    url='http://bitbucket.org/changer/cmsplugin-plaintext/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
