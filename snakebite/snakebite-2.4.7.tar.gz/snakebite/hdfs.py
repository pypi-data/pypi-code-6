

from snakebite.channel import ReadStream


class HDFS(object):
    def __init__(self, namenodes=None, config=None):
        pass

    class open(object):
        MODE_READ='r'
        MODE_WRITE='w'

        def __init__(self, path, mode=MODE_READ):
            self.path = path
            self.mode = mode
            self.stream = ReadStream(path)

        def __enter__(self):
            return self.stream

        def __exit__(self, type, value, traceback):
            self.stream.close()

        def read(self, size=None):
            if self.mode != MODE_READ:
                return self.stream.read(size)
            else:
                raise 'wrong mode!'

        def readline(self, size=None):
            pass

        def readlines(self, size=None):
            pass

        def write(self, str):
            pass

        def writelines(self, lines):
            pass
