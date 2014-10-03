from transit.writer import Writer
from StringIO import StringIO

io = StringIO()

writer = Writer(io, "json")
writer.write([2**53+100, 2**63+100])

s = io.getvalue()
print s
