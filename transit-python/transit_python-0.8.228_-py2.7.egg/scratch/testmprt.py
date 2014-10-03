from transit import reader, writer
from StringIO import StringIO

for fmt in ("msgpack", "json"):
    io = StringIO()
    w = writer.Writer(io, fmt)

    for item in [0, 1, 1902382]:
        w.write(item)

    io.seek(0)
    r = reader.Reader(fmt, io)

    for item in r.read():
        print(item)
