from transit.reader import Reader
from transit.writer import Writer
from StringIO import StringIO

s = 'a\nb'

io = StringIO()
writer = Writer(io, 'json')
writer.write(s)
output = io.getvalue()
io.close()

reader = Reader()
assert s == reader.read(StringIO(output))
