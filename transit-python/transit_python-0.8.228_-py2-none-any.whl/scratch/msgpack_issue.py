from transit.reader import Reader
from transit.writer import Writer
from StringIO import StringIO

mpcode = "94a37e6360a37e637ea37e635ea37e6323".decode("hex")

io = StringIO()
io.write(mpcode)
io.seek(0)
r = Reader(protocol="msgpack")
print(r.read(io))

