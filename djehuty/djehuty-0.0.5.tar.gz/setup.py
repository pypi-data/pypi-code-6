#!/usr/bin/env python
from setuptools import setup, find_packages


install_requires = [
    'pyramid==1.5.1',
    'cornice==0.16.2',
    'cliff==1.6.1',
]

setup(
    name='djehuty',
    version='0.0.5',
    description='POST web hook manager',
    author='xica development team',
    author_email='info@xica.net',
    url='https://github.com/xica/djehuty',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'djehuty = djehuty.app:main',
        ],
        'pyramid.scaffold': [
            'djehuty_server = djehuty.scaffolds:ServerTemplate',
            'djehuty_service = djehuty.scaffolds:ServiceTemplate',
            'djehuty_command = djehuty.scaffolds:CommandTemplate',
        ],
        'djehuty.commands': [
            'commands = djehuty.command.commands:Commands',
            'yo = djehuty.command.yo:Yo',
        ],
    }
)
