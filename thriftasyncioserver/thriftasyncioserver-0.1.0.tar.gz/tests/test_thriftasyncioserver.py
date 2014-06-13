#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_thriftasyncioserver
----------------------------------

Tests for `thriftasyncioserver` module.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/gen-py')

import unittest
from unittest import mock
import asyncio

from time import sleep
from test_service import TestService
from thriftasyncioserver import Server
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport
from threading import Thread, Event



class TestServerWrapper(object):
    thread = None
    server = None
    loop = None
    server_ready_event = None
    server_stop_event = None
        
    def __init__(self, *args, **kwargs):
        self.server = Server(*args, **kwargs)
        self.server_ready_event = Event()
        self.server_stop_event = Event()

        self.server.server_ready_event = self.server_ready_event
        self.server.server_stop_event = self.server_stop_event
        
    def server_thread_main(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.server.serve()
    
    def start(self):
        self.thread = Thread(target=self.server_thread_main)
        self.thread.daemon = True
        self.thread.start()
        self.server_ready_event.wait()
    
    def stop(self):
        self.loop.stop()
        self.server_stop_event.wait()
    

class BasicTests(unittest.TestCase):

    server = None
    client = None
    client_transport = None
    
    test_port = 42353
    test_host = 'localhost'
    def setUp(self):
        self.handler = mock.MagicMock()
        
        self.server = TestServerWrapper(
                             self.test_host,
                             self.test_port,
                             TBinaryProtocol.TBinaryProtocolFactory(),
                             TestService.Processor(self.handler))
        self.start_server()
        self.setup_client()
        
    def tearDown(self):
        
        self.destroy_client()
        self.stop_server()

    
    def setup_client(self):
        socket = TSocket.TSocket(self.test_host, self.test_port)
        self.client_transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.client_transport)
        self.client = TestService.Client(protocol)
        self.client_transport.open()
        
    def destroy_client(self):
        self.client_transport.close()
        
    def start_server(self):
        self.server.start()

    def stop_server(self):
        self.server.stop()
    
    def test_simple_ping(self):
        self.client.ping()
        self.handler.ping.assert_called_with()
    
    def test_simple_greet(self):
        self.handler.greet.return_value = 'hello world'
        self.assertEqual(self.client.greet('hello'), 'hello world')
        self.handler.greet.assert_called_with('hello')
    

if __name__ == '__main__':
    unittest.main()