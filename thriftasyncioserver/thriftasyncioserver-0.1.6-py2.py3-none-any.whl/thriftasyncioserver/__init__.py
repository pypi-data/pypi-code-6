# -*- coding: utf-8 -*-

__author__ = 'Thomas Bartelmess'
__email__ = 'tbartelmess@marketcircle.com'
__version__ = '0.1.6'

__all__ = ['Server']

import asyncio
from thrift.transport import TTransport


class Protocol(asyncio.Protocol):
    def __init__(self, protocol_factory, processor):
        self.protocol_factory = protocol_factory
        self.processor = processor
        self.input_buffer = TTransport.TMemoryBuffer(b'')

    def process_request(self):
        input_protocol = self.protocol_factory.getProtocol(self.input_buffer)
        out_buffer = TTransport.TMemoryBuffer()
        out_protocol = self.protocol_factory.getProtocol(out_buffer)
        self.processor.process(input_protocol, out_protocol)
        self.transport.write(out_buffer.getvalue())


    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """
        Callback when data is received.
        """
        self.input_buffer = TTransport.TMemoryBuffer(self.input_buffer.getvalue()+data)
        loop = asyncio.get_event_loop()
        self.process_request()


    def connection_lost(self, exc):
        self.transport.close()



class Server(object):
    """
    Thrift Server using the Python asyncio module.
    """

    server_ready_event = None
    server_stop_event = None

    def __init__(self, host, port, protocol_factory, processor, ssl=None):
        self.host = host
        self.port = port
        self.protocol_factory = protocol_factory
        self.processor = processor
        self.ssl = ssl

    def make_protocol(self):
        return Protocol(self.protocol_factory, self.processor)


    def make_server(self, loop):
        return loop.create_server(self.make_protocol,
                                  host = self.host,
                                  port = self.port,
                                  ssl = self.ssl)

    def serve(self):
        loop = asyncio.get_event_loop()

        coro = self.make_server(loop)

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

class UnixServer(Server):
    def __init__(self, path, ssl=None):
        self.path = path
        self.ssl = ssl

    def make_server(self, loop):
        return loop.create_unix_server(self.make_protocol, path=self.path)

