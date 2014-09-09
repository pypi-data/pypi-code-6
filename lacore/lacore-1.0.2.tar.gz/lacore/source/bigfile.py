import boto
import threading
import tempfile
import os
import sys
from collections import deque

DEFAULT_CHUNK_SIZE = 2**20 * 64  # 64 MB per request
MAX_CACHED = 5


class CachedChunksFile(object):
    """
    Wrap a file object that supports
    Original code from: http://stackoverflow.com/a/9015961/729491
    """

    def __init__(self, file_obj, file_size, chunksize=DEFAULT_CHUNK_SIZE,
                 start=True):
        self._file_obj = file_obj
        self._file_size = file_size
        self._lock = threading.RLock()
        self._load_condition = threading.Condition(self._lock)
        self._load_run = True
        self._loc = 0
        self._exc_info = None
        self._chunk_size = chunksize
        chunk_count = self._file_size // self._chunk_size
        chunk_count += 1 if self._file_size % self._chunk_size else 0
        self._chunks = [None for _ in xrange(chunk_count)]
        self._queue = deque(maxlen=MAX_CACHED)
        self._load_thread = threading.Thread(target=self._load)
        if start:
            self._load_thread.start()

    def _chunk_loc(self):
        """
         Returns (chunk_num, chunk_offset) for a given
         location in the larger file
        """
        return self._loc // self._chunk_size, self._loc % self._chunk_size

    def _load_chunk(self, chunk_num):
        tf = tempfile.TemporaryFile()
        start_idx = chunk_num * self._chunk_size
        self._file_obj.seek(start_idx)
        tf.write(self._file_obj.read(self._chunk_size))
        with self._lock:
            self._chunks[chunk_num] = (tf, tf.tell())  # (tempfile, size)
            if len(self._queue) == self._queue.maxlen:
                last = self._queue[-1]
                self._chunks[last][0].close()
                self._chunks[last] = None
            self._queue.appendleft(chunk_num)
            self._load_condition.notify()

    def _safe_load(self):
        try:
            self._load()
        except Exception:
            self._exc_info = sys.exc_info()

    def _load(self):
        while self._load_run:
            # check current chunk, load if needed
            with self._lock:
                self._load_condition.wait()  # wait till a read comes
                chunk_num, _ = self._chunk_loc()
                chunk_and_size = self._chunks[chunk_num]

            if chunk_and_size is None:
                self._load_chunk(chunk_num)

            # find next empty chunk
            for i in xrange(len(self._chunks)):
                cur_chunk = chunk_num + i
                cur_chunk %= len(self._chunks)  # loop around

                if self._chunks[cur_chunk] is None:
                    self._load_chunk(cur_chunk)
                    break
            else:
                # all done, stop thread
                break

    def seek(self, loc, rel=os.SEEK_SET):
        with self._lock:
            if rel == os.SEEK_CUR:
                self._loc += loc
            elif rel == os.SEEK_SET:
                self._loc = loc
            elif rel == os.SEEK_END:
                self._loc = self._file_size + loc

    def tell(self):
        return self._loc

    def _possibly_raise(self):
        if self._exc_info:
            try:
                raise self._exc_info[0], self._exc_info[1], self._exc_info[2]
            finally:
                self._exc_info = None

    def read(self, bytes_to_read=-1):
        ret = []
        if bytes_to_read < 0:
            bytes_to_read = self._file_size - self._loc
        with self._lock:
            chunk_num, chunk_offset = self._chunk_loc()
            while ((bytes_to_read > 0 or bytes_to_read == -1) and
                   chunk_num < len(self._chunks)):
                while not self._chunks[chunk_num]:
                    self._possibly_raise()
                    self._load_condition.notify()
                    self._load_condition.wait()
                chunk, size = self._chunks[chunk_num]
                cur_chunk_bytes = min(size-chunk_offset,
                                      bytes_to_read, size)
                chunk.seek(chunk_offset, os.SEEK_SET)
                data = chunk.read(cur_chunk_bytes)
                bytes_to_read -= len(data)
                ret.append(data)
                chunk_num += 1
                chunk_offset = 0
            ret = ''.join(ret)
            self._loc += len(ret)
        return ret

    def start(self):
        if self._load_thread.isAlive():
            return
        self._load_thread.start()

    def stop(self):
        self._load_run = False
        with self._lock:
            self._load_condition.notify()

    def __enter__(self):
        self._load_run = True
        self.start()
        return self

    def close(self):
        self.stop()
        self._load_thread.join(timeout=3)
        assert not self._load_thread.isAlive()

    def __exit__(self, type, value, traceback):
        self.close()


class S3RangeReader:
    def __init__(self, key_obj):
        self._key_obj = key_obj
        self.size = self._key_obj.size
        self._pos = 0

    def __len__(self):
        return self.size

    def seek(self, pos, rel=os.SEEK_SET):
        if rel == os.SEEK_CUR:
            self._pos += pos
        elif rel == os.SEEK_SET:
            self._pos = pos
        elif rel == os.SEEK_END:
            self._pos = self.size + pos

    def read(self, bytes=-1):
        if bytes == 0 or self._pos >= self.size:
            return ''
        else:
            if bytes == -1:
                bytes = self.size
            # S3 ranges are closed ranges: [start,end]
            headers = {'Range': 'bytes=%s-%s' % (
                self._pos, self._pos + bytes - 1)}
            return self._key_obj.get_contents_as_string(headers=headers)


class S3BackedFile(CachedChunksFile):
    def __init__(self, key, **kwargs):
        super(S3BackedFile, self).__init__(
            S3RangeReader(key), key.size, **kwargs)

if __name__ == '__main__':
    key = boto.connect_s3().get_bucket('lastage').get_key('foobarbig2')
    with S3BackedFile(key) as bf:  # download starts by default
        import zipfile
        with zipfile.ZipFile(bf) as z:
            for zi in z.infolist():
                print zi.filename
                z.extract(zi, '/tmp/')
