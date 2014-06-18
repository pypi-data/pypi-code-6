# -*- coding: utf8 -*-

from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(
      name='tsutil',
      version='0.1.4',
      py_modules=['tsutil.enum', 'tsutil.encoder', 'tsutil.util'],
      author='Turbidsoul Chen',
      author_email='sccn.sq+py@gmail.com',
      url='http://github.com/turbidsoul/tsutil',
      description='my python tool module',
      license='MIT',
      install_requires=reqs
)
