# -*- coding: utf-8 -*-
from transit.writer import Writer
from transit.reader import Reader
from transit.transit_types import URI
from StringIO import StringIO
import sys

io = StringIO()

x = URI(u'http://www.詹姆斯.com/')
print(x)

writer = Writer(io, protocol="json-verbose")
writer.write(x)
reader = Reader(protocol="json-verbose")
print io.getvalue()
io.seek(0)
outcome = reader.read(io)
print(outcome)


