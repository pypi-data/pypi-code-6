#coding=utf-8
__author__ = 'ldd'
from distutils.core import setup

setup(
      name='walleclient',
      version='0.1.0',
      py_modules=['walleclient'],
      author='ldd',
      author_email='dongdongl@oupeng.com',
      license='LGPL',
      install_requires=["beanstalkc>=0.4.0"],
      description="A client for walle",
      keywords ='walle client',
      url='http://oupeng.com/'
)