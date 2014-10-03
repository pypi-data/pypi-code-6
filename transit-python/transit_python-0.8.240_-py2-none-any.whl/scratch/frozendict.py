from transit.writer import Writer
from transit.reader import Reader
import StringIO

a={"a":1}
b={"a":1,"b":2}

io = StringIO.StringIO()
w = Writer(io, protocol="msgpack")

w.write([a,b])
r = Reader(protocol="msgpack")
result = r.read(StringIO.StringIO(io.getvalue()))
print result
