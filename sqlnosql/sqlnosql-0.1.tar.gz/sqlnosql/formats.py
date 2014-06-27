from sqlalchemy.types import BOOLEAN, INTEGER, FLOAT, TEXT, DATE, DATETIME, TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY, JSON

def union(*args):
    items = []
    for arg in args:
        items.extend(arg.items())
    return dict(items)

# note: using varchar has no performance advantage in postgres, so we 
# can always just store strings in text fields
TYPES = {
    'boolean': BOOLEAN, 
    'integer': INTEGER, 
    'number': FLOAT, 
    'string': TEXT, 
    'array': TEXT, 
    'object': TEXT, 
}

TYPE_EXTENSIONS = {
    'array': ARRAY, 
    'object': JSON, 
}

FORMATS = {
    'date': DATE, 
    'date-time': DATETIME, 
    'timestamp': INTEGER, 
}

FORMAT_EXTENSIONS = {
    'timestamp': TIMESTAMP,     
}

generic = union(TYPES, FORMATS)
postgresql = union(TYPES, TYPE_EXTENSIONS, FORMATS, FORMAT_EXTENSIONS)