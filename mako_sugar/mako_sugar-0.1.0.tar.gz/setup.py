# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='mako_sugar',
    version='0.1.0',
    author=u'Marc Paré',
    author_email='marc@smallredtile.com',
    packages=find_packages('.', exclude=['test*']),
    license='MIT',
    url='https://github.com/marcpare/mako-sugar',
    download_url='https://github.com/marcpare/mako-sugar/tarball/0.1.0',
    description='Syntax sugar for Python Mako templates',
    long_description=open('README.md').read(),
    zip_safe=False,
)