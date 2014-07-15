import sqlnosql
from gnulynx.serialize import from_yaml, from_json

def get_types(schemafile, **kw):
  """
  Create a dictionary of sqlalchemy types a jsonschema file via sqlnosql
  """
  # Load schemafile 
  if schemafile:
    if schemafile.endswith('yml') or schemafile.endswith('yaml'):
      schema = from_yaml(open(schemafile).read())
    elif schemafile.endswith('json'):
      schema = from_json(open(schemafile).read())

    # create types dictionary
    types = sqlnosql.schema.create_types(schema, **kw)
    return types
    
  else:
    return {}

