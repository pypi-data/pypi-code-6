from setuptools import setup

description = open('tornrpc/README').read()

setup(
  name='TornRPC',
  version='1.0.2',
  description='A tornado RPC framework',
  long_description=description,
  author='Kyle Laplante',
  author_email='kyle.laplante@gmail.com',
  keywords='rpc tornado asynchronous web',
  packages=['tornrpc'],
  install_requires=['tornado'],
)
