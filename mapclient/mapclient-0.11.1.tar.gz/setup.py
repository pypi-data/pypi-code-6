#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    import PySide
    pyside_version = PySide.__version__
    pyside_requirement = 'PySide==' + pyside_version
except ImportError:
    pyside_requirement = 'PySide'

install_requires = [
        pyside_requirement,
        'requests-oauthlib',
        'pmr.wfctrl']

try:
    import importlib
except ImportError:
    install_requires.append('importlib')

setup(name='mapclient',
     version='0.11.1',
     description='A framework for managing and sharing workflows.',
     author='MAP Client Developers',
     author_email='mapclient-devs@physiomeproject.org',
     url='https://launchpad.net/mapclient',
     namespace_packages=['mapclient', ],
     packages=find_packages(exclude=['tests', 'tests.*', ]),
     package_data={'mapclient.tools.annotation': ['annotation.voc']},
     # py_modules=['mapclient.mapclient'],
     entry_points={'console_scripts': ['mapclient=mapclient.application:winmain']},
     install_requires=install_requires
)
