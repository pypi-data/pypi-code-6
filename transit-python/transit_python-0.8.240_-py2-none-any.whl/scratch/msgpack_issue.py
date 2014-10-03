from transit.reader import Reader
from transit.writer import Writer
from StringIO import StringIO

#json = "{\"~#set\":[{\"~#set\":[1,3,2]},{\"~#set\":[null,0,2.0,\"~~eight\",1,true,\"five\",false,\"~$seven\",\"~:six\"]}]}\n"
#mpcode = "94a37e6360a37e637ea37e635ea37e6323".decode("hex")

json = "{\"~#set\":[1,true]}"
io = StringIO()
io.write(json)
io.seek(0)
r = Reader(protocol="json")
correct = r.read(io)
out = StringIO()
w = Writer(out, protocol="json")
w.write(correct)
print(json)
print(out.getvalue())

