# -*- coding: utf-8 -*-
import os, re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

v = open(os.path.join(here, 'pyramid_js', '__init__.py'))
version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()


setup(
    name='pyramid-js',
    version=version,
    author='Stéphane Klein',
    author_email='contact@stephane-klein.info',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['pyramid', 'MarkupSafe']
)
