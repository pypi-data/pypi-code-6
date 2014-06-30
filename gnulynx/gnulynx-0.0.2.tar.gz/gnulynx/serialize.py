import yaml
import json 

## TODO MAKE THESE BETTER 

def json_from_string(s):
  return json.loads(s)

def json_to_string(obj):
  return json.dumps(obj)

def yaml_from_string(s):
  return yaml.safe_loads(s)