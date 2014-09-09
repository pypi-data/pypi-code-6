import io
import requests
import os.path

from itertools import imap
from .stream import StreamArchiver
from contextlib import closing


def iterable_to_stream(iterable, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """
    Lets you use an iterable (e.g. a generator) that yields bytestrings as a
    read-only input stream.

    The stream implements Python 3's newer I/O API (available in Python 2's io
    module).  For efficiency, the stream is buffered.

    From: http://stackoverflow.com/a/20260030/729491
    """
    class IterStream(io.RawIOBase):
        def __init__(self):
            self.leftover = None

        def readable(self):
            return True

        def readinto(self, b):
            try:
                l = len(b)  # We're supposed to return at most this much
                chunk = self.leftover or next(iterable)
                output, self.leftover = chunk[:l], chunk[l:]
                b[:len(output)] = output
                return len(output)
            except StopIteration:
                return 0    # indicate EOF
    return io.BufferedReader(IterStream(), buffer_size=buffer_size)


class UrlArchiver(StreamArchiver):
    url_chunk = io.DEFAULT_BUFFER_SIZE

    def __init__(self, url_chunk=None, progress_cb=None, *args, **kwargs):
        if url_chunk is not None:
            self.url_chunk = url_chunk
        self.progress_cb = progress_cb
        super(UrlArchiver, self).__init__(*args, **kwargs)

    def closing_url(self, url, rel):
        with closing(requests.get(url, stream=True)) as r:
            for c in r.iter_content(chunk_size=self.url_chunk):
                yield c

    def url_to_stream(self, item):
        try:
            url, rel = item
        except:
            url = item
            rel = os.path.basename(item.strip('/'))
        r = iterable_to_stream(self.closing_url(url, rel))
        return (r, rel)

    def args(self, items, cb):
        return super(UrlArchiver, self).args(
            imap(self.url_to_stream, items), cb)
