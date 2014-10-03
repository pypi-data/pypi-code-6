# -*- coding: utf-8 -*-
from transit.writer import Writer
from transit.reader import Reader
from transit.transit_types import URI
from StringIO import StringIO
import sys

io = StringIO()

x = set()
print(x)

writer = Writer(io, protocol="json")
writer.write(x)
reader = Reader(protocol="json")
print io.getvalue()
io.seek(0)
outcome = reader.read(io)
print(outcome)
