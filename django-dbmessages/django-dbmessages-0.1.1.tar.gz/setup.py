#coding: utf-8

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-dbmessages',
    version='0.1.1',
    packages=['dbmessages'],
    include_package_data=True,
    license='BSD License',
    description='Request-independent messaging for Django on top of contrib.messages',
    long_description=README,
    author='oDesk',
    author_email='python@odesk.com',
    maintainer='Anton Strogonoff',
    maintainer_email='anton@strogonoff.name',
    download_url='http://github.com/strogonoff/django-dbmessages',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
