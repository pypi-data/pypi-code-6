import functools
from StringIO import StringIO
from json import dumps as dumps_json
import csvkit
import formats

def defaults(serializer):
    @functools.wraps(serializer)
    def serialized_with_defaults(value, dialect='generic', **kwargs):
        dialect = getattr(formats, dialect)

        if isinstance(value, list) and dialect['array'] == dialect['string']:
            return serializer(value, **kwargs)
        elif isinstance(value, dict) and dialect['object'] == dialect['string']:
            return serializer(value, **kwargs)
        else:
            return value        

    return serialized_with_defaults

@defaults
def json(value):
    if isinstance(value, list) or isinstance(value, dict):
        return dumps_json(value)
    else:
        return value

def dumps_csv(value):
    buf = StringIO()
    writer = csvkit.writer(buf)
    writer.writerow(value)
    value = buf.getvalue().strip()
    buf.close()
    return value

@defaults
def csv(value):
    if isinstance(value, list):
        return dumps_csv(value)
    elif isinstance(value, dict):
        kvs = map("=".join, value.items())
        return dumps_csv(kvs)
    else:
        return value