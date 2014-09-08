class Stream(object):
    def read(self):
        yield 'a'
        yield 'b'

    def close(self):
        print 'closing'

class myopen(object):
    def __init__(self, path):
        self.path = path
        self.s = Stream()
        print 'craete myopen with %s' % path

    def read(self):
        return self.s.read()

    def __enter__(self):
        print 'just entered'
        return self.s

    def __exit__(self, type, value, traceback):
        self.s.close()
        print 'exit!'

    def __repr__(self):
        return "<hdfs open file '%s', mode 'r' at %s>" % (self.path, hex(id(self)))

#if __name__ == '__main__':
d = myopen('d')
s = d.read()
