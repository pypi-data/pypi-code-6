import os
import sys
from distutils.core import setup

setup(
    name =  'qiniufops',
    version='0.1',
    author = 'Augmentum OPS team',
    author_email = 'ops@jinyuntian.com',
    description = 'Qiniu bucket image persistent operations',
    scripts = ['qiniufops'],
    install_requires=['qiniu'],
    data_files = [
        ('/etc/qiniu/',['qiniufops.cfg']),
        ('/etc/qiniu/',['README.md'])
    ]
)