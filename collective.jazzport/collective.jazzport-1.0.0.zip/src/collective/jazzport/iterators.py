# -*- coding: utf-8 -*-
from ZPublisher.Iterators import IStreamIterator
from ZServer.PubCore.ZEvent import Wakeup
from zope.interface import implements
import StringIO
import threading


class zhttp_channel_async_wrapper(object):
    """Medusa channel wrapper to defer producers until released"""

    def __init__(self, channel):
        # (executed within the current Zope worker thread)

        self._channel = channel

        self._mutex = threading.Lock()
        self._deferred = []
        self._released = False
        self._content_length = 0
        self._content_type = None
        self._content_filename = None

    def _push(self, producer, send=1):
        if (isinstance(producer, str)
                and producer.startswith('HTTP/1.1 200 OK')):
            # Fix response headers to match the final content:
            s = str(self._content_length)
            if self._content_type:
                s += '\r\nContent-Type: {0:s}'.format(self._content_type)
            if self._content_filename:
                s += '\r\nContent-Disposition: attachment; filename="{0:s}"'\
                    .format(self._content_filename)
            producer = producer.replace(
                'Content-Length: 0\r\n',
                'Content-Length: {0:s}\r\n'.format(s)
            )
        self._channel.push(producer, send)

    def push(self, producer, send=1):
        # (executed within the current Zope worker thread)

        with self._mutex:
            if not self._released:
                self._deferred.append((producer, send))
            else:
                self._push(producer, send)

    def release(self, content_length, content_type, content_filename):
        # (executed within the exclusive async thread)

        self._content_length = content_length
        self._content_type = content_type
        self._content_filename = content_filename

        with self._mutex:
            for producer, send in self._deferred:
                self._push(producer, send)
            self._released = True
        Wakeup()  # wake up the asyncore loop to read our results

    def __getattr__(self, key):
        return getattr(self._channel, key)


class AsyncWorkerStreamIterator(StringIO.StringIO):
    """Stream iterator to publish the results of the given func"""

    implements(IStreamIterator)

    def __init__(self, func, request, streamsize=1 << 16):
        # (executed within the current Zope worker thread)

        # Init buffer
        StringIO.StringIO.__init__(self)
        self._streamsize = streamsize

        # Wrap the Medusa channel to wait for the func results
        response = request.response
        self._channel = response.stdout._channel
        self._wrapped_channel = zhttp_channel_async_wrapper(self._channel)
        response.stdout._channel = self._wrapped_channel

        # Set content-length as required by ZPublisher
        response.setHeader('content-length', '0')

        # Fire the given func in a separate thread
        self.thread = threading.Thread(target=func, args=(self.callback,))
        self.thread.start()

    def callback(self, data, content_type, content_filename):
        # (executed within the exclusive async thread)

        self.write(data)
        self.seek(0)
        self._wrapped_channel.release(
            len(data), content_type, content_filename)

    def next(self):
        # (executed within the main thread)

        if not self.closed:
            data = self.read(self._streamsize)
            if not data:
                self.close()
            else:
                return data
        raise StopIteration

    def __len__(self):
        return len(self.getvalue())