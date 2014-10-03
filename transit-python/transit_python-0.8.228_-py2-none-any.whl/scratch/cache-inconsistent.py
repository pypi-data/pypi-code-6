from StringIO import StringIO
from transit.writer import Writer
from transit.reader import Reader
from transit.transit_types import Symbol
r = Reader('json')
io = StringIO()
w = Writer(io,'json')
w.write([{"Problem?":True},Symbol("Here"),Symbol("Here")])
print(io.getvalue())
print(r.read(StringIO(io.getvalue())))
