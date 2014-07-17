# -*- coding: utf8 -*-

from setuptools import setup

reqs = ['requests==2.3.0', 'chardet==2.1.1']

setup(
      name='tsutil',
      version='0.1.6.1',
      py_modules=['tsutil.enum', 'tsutil.encoder', 'tsutil.util', 'tsutil.daemonize'],
      author='Turbidsoul Chen',
      author_email='sccn.sq+py@gmail.com',
      url='http://github.com/turbidsoul/tsutil',
      description='my python tool module',
      license='MIT',
      install_requires=reqs,
      package_dir={'':'.'},
      include_package_data=True,
      package_data = {'require': ['*.txt']}
)

