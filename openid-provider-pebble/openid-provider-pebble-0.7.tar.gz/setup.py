# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = "openid-provider-pebble",
    version = "0.7",
    author = u"Pebble",
    author_email = "dev@mypebble.co.uk",
    description = "Pebble fork of django_openid_provider",
    long_description = open("README.txt").read(),
    license = "Apache",
    url = "http://django-openid-provider.readthedocs.org/",
    download_url = "https://bitbucket.org/romke/django_openid_provider",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
