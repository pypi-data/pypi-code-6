import copy
import utils
import formats
import serializers
from sqlalchemy import Table, Column


def create(schema, dialect='generic', connector='_', parent_key='', is_required=False):
    """ Turns a JSON schema into a list of columns and SQL types. """

    TYPES = getattr(formats, dialect)

    if not parent_key:
        schema = copy.copy(schema)

    format = schema.get('format') or schema['type']

    if format == 'object' and not 'properties' in schema:
        return [(parent_key, TYPES[format], is_required)]
    elif format == 'array':
        if TYPES['array'] == TYPES['string']:
            array = TYPES['array']
        else:
            array = TYPES['array'](TYPES[schema['items']['type']])
        return [(parent_key, array, is_required)]
    elif format != 'object' and format in TYPES:
        return [(parent_key, TYPES[format], is_required)]
    else:
        types = []
        for key, value in schema['properties'].items():
            if parent_key:
                name = connector.join([parent_key, key])
            else:
                name = key

            subschema = schema['properties'][key]
            subschema_required = key in schema.get('required', [])
            types.extend(create(subschema, 
                dialect=dialect, 
                connector=connector, 
                parent_key=name, 
                is_required=subschema_required))

        return types

def keys(schema, dialect='generic'):
    return map(utils.first, create(schema, dialect))

def create_table(schema, metadata, name=None, pk='', dialect='generic'):
    if not name:
        if 'title' in schema:
            name = utils.slugify(schema['title'])
        else:
            raise KeyError('title')

    pk = pk.replace('.', '_')

    def is_pk(definition):
        key = definition[0]
        return (key, key == pk)

    definitions = create(schema, dialect)
    pks = dict(map(is_pk, definitions))
    columns = [Column(colname, coltype, nullable=(not required), primary_key=pks[colname]) 
        for colname, coltype, required in definitions]

    return Table(name, metadata, *columns)

def deflate(obj, schema=None, dialect='generic'):
    if schema:
        allowed = skip = keys(schema)
    else:
        allowed = skip = []

    # to make sure the database doesn't choke on fields
    # that shouldn't be there (and also just to make 
    # sure we adhere to the schema), delete all 
    # fields not present in the schema
    deflated_obj = utils.deflate(obj, skip)
    for key in deflated_obj.keys():
        if not key in allowed:
            del deflated_obj[key]

    return deflated_obj

def serialize(obj, schema=None, dialect='generic', serializer=serializers.json):
    deflated_obj = deflate(obj, schema)
    keys = deflated_obj.keys()
    values = map(serializer, deflated_obj.values())
    return dict(zip(keys, values))
