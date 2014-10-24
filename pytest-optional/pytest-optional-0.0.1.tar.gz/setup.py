#!/usr/bin/env python
from setuptools import setup


setup(
        name='pytest-optional',
        version='0.0.1',
        description='include/exclude values of fixtures in pytest',
        author='Maho',
        author_email='maho@pagema.net',
        url='http://bitbucket.org/maho/pytest-optional',
        download_url= 'https://bitbucket.org/maho/pytest-optional/get/default.tar.gz',
        install_requires = ['decorator'],
        packages=['pytest_optional'],
        include_package_data=True,
        package_data = {
        },
        keywords = ['pytest'],
)
