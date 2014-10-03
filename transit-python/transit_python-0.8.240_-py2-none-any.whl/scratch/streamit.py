from StringIO import StringIO
from copy import copy
import json

DELIMS = {"{" : "}",
          "[" : "]",
          "\"": "\""}

SKIP = [" ", "\n", "\t"]

ESCAPE = "\\"

def read_chunk(stream):
    """Ignore whitespace outside of strings.
    """
    chunk = stream.read(1)
    while chunk in SKIP:
        chunk = stream.read(1)
    if chunk == "\"":
        chunk += stream.read(1)
        while not chunk.endswith("\""):
            if chunk[-1] == ESCAPE:
                chunk += stream.read(2)
            else:
                chunk += stream.read(1)
    return chunk

def yield_json(stream):
    buff = u""
    arr_count = 0
    obj_count = 0
    while True:
        buff += read_chunk(stream)

        if buff.endswith('{'):
            obj_count += 1
        if buff.endswith('['):
            arr_count += 1
        if buff.endswith(']'):
            arr_count -= 1
            if obj_count == arr_count == 0:
                json_item = copy(buff)
                buff = u""
                yield json_item
        if buff.endswith('}'):
            obj_count -= 1
            if obj_count == arr_count == 0:
                json_item = copy(buff)
                buff = u""
                yield json_item

if __name__ == "__main__":
    x = StringIO("""[\"^ \",\"~:key0000\",0,\"~:key0001\",1,\"~:key0002\",2,\"~:key0003\",3,\"~:key0004\",4,\"~:key0005\",5,\"~:key0006\",6,\"~:key0007\",7,\"~:key0008\",8,\"~:key0009\",9]\n""")
#    x = StringIO("""{\"~#'\":false}\n""")
    for a in yield_json(x):
        print(a)
