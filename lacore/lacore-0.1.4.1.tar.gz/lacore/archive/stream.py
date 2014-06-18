import io

from .zip import ZipArchiver
from functools import partial
from collections import OrderedDict


class ProgressStream(io.RawIOBase):
    def __init__(self, fp, progress=None):
        self.fp = fp
        self.progress = progress
        self.leftover = None

    def readable(self):
        return True

    def readinto(self, b):
        l = len(b)  # We're supposed to return at most this much
        chunk = self.leftover or self.fp.read(l)
        if chunk is None:
            return None
        output, self.leftover = chunk[:l], chunk[l:]
        b[:len(output)] = output
        if self.progress is not None:
            self.progress(output)
        return len(output)

    def close(self):
        super(ProgressStream, self).close()
        self.fp.close()


class StreamArchiver(ZipArchiver):
    processed = None
    stream_chunk = io.DEFAULT_BUFFER_SIZE

    def process(self, rel, data):
        self.processed[rel] += len(data)

    def __init__(self, stream_chunk=None, progress_cb=None, *args, **kwargs):
        if stream_chunk is not None:
            self.stream_chunk = stream_chunk
        self.progress_cb = progress_cb
        super(StreamArchiver, self).__init__(*args, **kwargs)

    def args(self, items, cb):
        self.processed = OrderedDict()
        for stream, rel in items:
            self.processed[rel] = 0
            if cb is not None:
                cb(stream, rel)
            s = io.BufferedReader(
                ProgressStream(
                    stream, partial(self.process, rel)),
                self.stream_chunk)
            yield ((s,), {'arcname': rel.encode('utf-8')})
