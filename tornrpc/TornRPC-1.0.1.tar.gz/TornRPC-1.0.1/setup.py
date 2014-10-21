from setuptools import setup

description = """
A tornado RPC library. 

This RPC framework uses tornado
so its very quick and asynchronous.

Example:
### example server code ###

from tornado import gen
from tornrpc.server import TornRPCServer


def test(arg):
  return "You said %s" % arg

@gen.coroutine
def testasync(arg):
  return "You said async %s" % arg

server = TornRPCServer()
server.register(test)
server.register_async(testasync)
server.start(8080)


### example client code ###

from tornrpc.client import TornRPCClient

client = TornRPCClient('localhost:8080')
client.test('hi')
client.testasync('hi')
"""

setup(
  name='TornRPC',
  version='1.0.1',
  description='A tornado RPC framework',
  long_description=description,
  author='Kyle Laplante',
  author_email='kyle.laplante@gmail.com',
  keywords='rpc tornado asynchronous web',
  packages=['tornrpc'],
  install_requires=['tornado'],
)
