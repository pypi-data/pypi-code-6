# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-pluggable-filebrowser',
    version='3.5.8',
    description='Pluggable Django Media-Management.',
    long_description = read('README.rst'),
    url = 'https://github.com/jinzo/django-pluggable-filebrowser',
    download_url='',
    author='Matjaž Črnko, Patrick Kranzlmueller, Axel Swoboda (vonautomatisch)',
    author_email='matjaz.crnko@gmail.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    zip_safe = False,
    install_requires = [
        'django>=1.4',
    ],
)
