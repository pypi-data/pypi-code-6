#! /usr/bin/env python
#coding: utf-8

import sys
import os
import subprocess
from distutils.core import setup

p = subprocess.Popen("gitbook -V > /dev/null 2>&1", shell=True)
r = p.wait()
if not r == 0:
    print '    Your system has not install gitbook,please install it at first.'

NAME = 'docbook'
DESCRIPTION = 'Generate docbook and upload qiniu to read online '
AUTHOR = 'Augmentum OPS team'
AUTHOR_EMAIL = 'ops@jinyuntian.com'

def version():
    with open('./VERSION') as ver:
        return ver.readline().split('v')[1]

setup(
    name=NAME,
    version=version(),
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    platforms='any',
    scripts = ['docbook','docbook_clean'],
    install_requires=['qiniu'],
    data_files = [
        ('/etc/docbook/',['./docbook']),
        ('/etc/docbook/',['./docbook_clean']),
        ('/etc/docbook/',['./docbook.conf']),
        ('/etc/docbook/',['./CHANGELOG.md']),
        ('/etc/docbook/',['./INSTALL.md']),
        ('/etc/docbook/',['./LICENSE.md']),
        ('/etc/docbook/',['./README.md']),
        ('/etc/docbook/',['./VERSION'])]
)
