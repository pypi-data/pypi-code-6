# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="m3-pushme",
    version="0.1.5",
    description='Подсистема доставки сообщений от сервера браузеру',
    license='MIT',
    author="Alexey Pirogov",
    author_email="pirogov@bars-open.ru",
    url="https://bitbucket.org/barsgroup/pushme",
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
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=[
        'sockjs-tornado',
        'snakemq'
    ],
)
