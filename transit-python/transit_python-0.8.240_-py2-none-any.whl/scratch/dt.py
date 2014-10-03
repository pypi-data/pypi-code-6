from transit.writer import Writer
from StringIO import StringIO
import datetime as dt

io = StringIO()
writer = Writer(io, "json")
writer.write({"date": dt.datetime.utcnow()})
