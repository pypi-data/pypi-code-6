import io
import os
import asyncio

from collections import deque


def pipe():
    loop = asyncio.get_event_loop()
    reader, writer = os.pipe()

    reader = Connection(os.fdopen(reader, 'rb', 0))
    writer = Connection(os.fdopen(writer, 'wb', 0))

    loop.run_until_complete(reader._connect(loop))
    loop.run_until_complete(writer._connect(loop))

    return reader, writer


class Connection(object):
    def __init__(self, handler):
        self._data = deque()
        self._stream_buffer = b''
        self._handler = handler
        self._reader = None
        self._writer = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    @asyncio.coroutine
    def _connect(self, loop):
        if self._handler.mode == 'rb':
            self._reader = asyncio.StreamReader(loop=loop)
            protocol = asyncio.StreamReaderProtocol(self._reader, loop=loop)
            yield from loop.connect_read_pipe(lambda: protocol, self._handler)
        else:
            trns, prot = yield from loop.connect_write_pipe(asyncio.Protocol,
                                                            self._handler)
            self._writer = asyncio.StreamWriter(trns, prot, None, loop)

    @asyncio.coroutine
    def _receive(self):
        """Receives data from the other side of the connection
        and deserializes it.

        """
        cursor = 0
        data = yield from self._reader.read(BUFFSIZE)
        stream = io.BytesIO(self._stream_buffer + data)

        while 1:
            try:
                cursor = stream.tell()
                self._data.append(load(stream))
            except EOFError:
                stream.seek(cursor)
                self._stream_buffer = stream.read()
                return

    def _closed(self):
        if self.closed:
            raise OSError("handle is closed")

    def _readable(self):
        if not self.readable:
            raise OSError("connection is write-only")

    def _writable(self):
        if not self.writable:
            raise OSError("connection is read-only")

    @property
    def closed(self):
        """True if the connection is closed"""
        return self._handle is None

    @property
    def readable(self):
        """True if the connection is readable"""
        if self._handle is not None:
            return self._handler.mode == 'rb' and True or False
        else:
            return False

    @property
    def writable(self):
        """True if the connection is writable"""
        if self._handle is not None:
            return self._handler.mode == 'rb' and True or False
        else:
            return False

    @asyncio.coroutine
    def poll(self, timeout=None):
        self._closed()
        self._readable()

        try:
            yield from asyncio.wait_for(self._receive(), timeout)
        except asyncio.TimeoutError:
            pass

        return self._data and True or False

    @asyncio.coroutine
    def recv(self):
        self._closed()
        self._readable()

        if not self._data:
            yield from self._receive()

        return self._data.popleft()

    def fileno(self):
        """File descriptor or handle of the connection"""
        self._closed()
        return self._handle

    def close(self):
        """Close the connection"""
        if self._handle is not None:
            try:
                self._close()
            finally:
                self._handle = None

    def send(self, obj):
        self._closed()
        self._writable()

        self._writer.write(dumps(obj))
