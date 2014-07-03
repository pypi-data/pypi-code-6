import yaml
import ujson 

## TODO MAKE THESE BETTER / ADD TYPE DETECTION ON LOAD.

def json_from_string(s):
  return ujson.loads(s)

def json_to_string(obj):
  return ujson.dumps(obj)

def yaml_from_string(s):
  return yaml.safe_loads(s)

def json_from_lines(l):
  return [json_from_string(i) for i in l if i.strip() != '']

def json_to_lines(l):
  if isinstance(l, list):
    return "\n".join([json_to_string(i) for i in l])
    
  elif isinstance(l, dict):
    return "\n".join([json_from_string(l)])
