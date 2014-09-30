# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

if os.environ.get('USER', '') == 'vagrant':
    del os.link

setup(name="sd-cli",
      version="0.1.1",
      description="Command line interface for Server Density",
      author=u"Bahadır Kandemir",
      author_email="kandemir@gmail.com",
      url="https://github.com/bahadir/sd-cli",
      packages=find_packages(),
      scripts=['sd'])
