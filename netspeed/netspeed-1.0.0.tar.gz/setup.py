#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-11-03 22:49:32
# Filename        : setup.py
# Description     : 

from distutils.core import setup
setup(
    name = 'netspeed',
    version = '1.0.0',
    author = 'tuxpy',
    author_email = 'q8886888@qq.com',
    license = 'GPL3',
    description = 'Display interface speed',
    url = 'https://github.com/lujinda/netspeed',
    packages = [
        'netspeed',
        'netspeed.ui',
        'netspeed.core',
        ],
    scripts = ['bin/netspeed'],
        )
