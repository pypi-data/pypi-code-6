import yaml
import ujson 

## TODO MAKE THESE BETTER / ADD TYPE DETECTION ON LOAD.


def to_json(obj):
  return ujson.dumps(obj)


def from_json(s):
  return ujson.loads(s)


def from_yaml(s):
  return yaml.load(s)


def to_yaml(obj):
  return yaml.dumps(obj)


def from_jsonlines(l):
  for i in l:
    if i.strip() != '':
      yield json_from_string(i)


def to_jsonlines(l):
  if isinstance(l, list):
    return "\n".join([json_to_string(i) for i in l])
    
  elif isinstance(l, dict):
    return "\n".join([json_from_string(l)])
