# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="m3-objectpack",
    version="0.7.3.7",
    description=read('DESCRIPTION'),
    license="GPL",
    keywords="django m3 m3-contrib",

    author="Alexey Pirogov",
    author_email="pirogov@bars-open.ru",

    maintainer='Alexey V Pirogov, Rinat F Sabitov',
    maintainer_email='rinat.sabitov@gmail.com',

    url="https://bitbucket.org/barsgroup/objectpack",
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
    ],
    packages=find_packages(exclude=['example', 'example.*']),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
)
