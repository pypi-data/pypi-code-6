# -*- coding: utf-8 -*-

__author__ = 'Thomas Bartelmess'
__email__ = 'tbartelmess@marketcircle.com'
__version__ = '0.1.0'

__all__ = ['Server']

import asyncio
import threading
from thrift.transport import TTransport


class Protocol(asyncio.Protocol):
    def __init__(self, protocol_factory, processor):
        self.protocol_factory = protocol_factory
        self.processor = processor
        self.input_buffer = TTransport.TMemoryBuffer

    def connection_made(self, transport):
        self.transport = transport

    def process_request(self, input_buffer):
        input_protocol = self.protocol_factory.getProtocol(input_buffer)
        out_buffer = TTransport.TMemoryBuffer()
        out_protocol = self.protocol_factory.getProtocol(out_buffer)
        self.processor.process(input_protocol, out_protocol)
        self.transport.write(out_buffer.getvalue())

    def data_received(self, data):
        """
        Callback when data is received.
        """
        input_buffer = TTransport.TMemoryBuffer(data)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.process_request, input_buffer)

    def connection_lost(self, exc):
        self.transport.close()

class Server(object):
    """
    Thrift Server using the Python asyncio module.
    """
    
    server_ready_event = None
    server_stop_event = None
    
    def __init__(self, host, port, protocol_factory, processor):
        self.host = host
        self.port = port
        self.protocol_factory = protocol_factory
        self.processor = processor

    def make_protocol(self):
        return Protocol(self.protocol_factory, self.processor)

    def serve(self):
        loop = asyncio.get_event_loop()

        coro = loop.create_server(self.make_protocol, self.host, self.port)
        
        server = loop.run_until_complete(coro)
        if self.server_ready_event:
            self.server_ready_event.set()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
            loop.run_until_complete(server.wait_closed())            
            if self.server_stop_event:
                self.server_stop_event.set()
