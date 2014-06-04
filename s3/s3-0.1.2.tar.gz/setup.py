# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
        name='s3',
        version='0.1.2',
        description="Python module which connects to Amazon's S3 REST API",
        long_description=open('README.rst', 'r').read(),
        author='Paul Wexler',
        author_email="paul@prometheusresearch.com",
        license="MIT",
        url='https://bitbucket.org/prometheus/s3/',
        classifiers=[
                'Programming Language :: Python',
                'Intended Audience :: Developers',
                 ],
        platforms='Any',
        keywords=('amazon', 'aws', 's3', 'upload', 'download'),
        package_dir={'': 'src'},
        packages=find_packages('src'),
        install_requires=[
                'requests >= 1.2.0', 
                'futures >= 2.1.3', 
                'xmltodict >= 0.9.0', 
                ] 
        )

