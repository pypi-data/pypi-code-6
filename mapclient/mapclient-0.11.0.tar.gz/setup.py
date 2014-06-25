#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='mapclient',
     version='0.11.0',
     description='A framework for managing and sharing workflows.',
     author='MAP Client Developers',
     author_email='mapclient-devs@physiomeproject.org',
     url='https://launchpad.net/mapclient',
     namespace_packages=['mapclient', ],
     packages=find_packages(exclude=['tests', 'tests.*', ]),
     package_data={'mapclient.tools.annotation': ['annotation.voc']},
     #py_modules=['mapclient.mapclient'],
     entry_points={'console_scripts': ['mapclient=mapclient.application:winmain']},
     install_requires=[
        'PySide',
        'requests-oauthlib',
        'pmr.wfctrl',
    ],
)
